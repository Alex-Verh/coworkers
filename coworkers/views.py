from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser, WorkerLanguage, WorkerNationality, Trait, WorkerTrait
from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ExperienceForm, ContactForm, FullNameUpdateForm, SalaryUpdateForm, LocationUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.edit import FormView, View
from .mixins import ExperienceFormMixin, ContactFormMixin
from django.core.mail import EmailMessage
import json
from django.conf import settings


class IndexView(generic.ListView, ContactFormMixin):
    template_name = "index.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_section'] = self.get_queryset()[:6]  # first section
        context['users_paginated'] = self.get_queryset()   # second section
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            page_number = request.GET.get('page', 1)
            paginator = Paginator(CustomUser.objects.all(), 3)
            page_obj = paginator.get_page(page_number)

            users_data = [
                {
                    "id": user.id,
                    "full_name": user.full_name,
                    "position": user.position,
                    "experience": user.experience,
                }
                for user in page_obj
            ]

            return JsonResponse({
                "users": users_data,
                "has_next": page_obj.has_next()
            })

        return super().get(request, *args, **kwargs)
    

class ProfileView(LoginRequiredMixin, ExperienceFormMixin, ContactFormMixin, generic.DetailView):
    model = CustomUser
    template_name = "profile.html"
    context_object_name = 'user'

    def get_object(self, queryset=None):
        """Retrieve the user object based on the URL or the logged-in user."""
        if 'pk' in self.kwargs:
            return get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        section = self.request.GET.get("section", "personal-data")

        user_languages = WorkerLanguage.objects.filter(user=user).select_related('language')
       
        user_nationalities = WorkerNationality.objects.filter(user=user).select_related('nationality')

        user_trait_measure  = WorkerTrait.objects.filter(
        user=user,
        trait=OuterRef('pk')
        ).values('trait_measure')[:1]

        personal_attributes = Trait.objects.annotate(
            user_score=Coalesce(Subquery(user_trait_measure, output_field=IntegerField()), Value(1))
        )

        # forms
        context['full_name_form'] = FullNameUpdateForm(instance=user)
        context['salary_form'] = SalaryUpdateForm(instance=user)
        context['location_form'] = LocationUpdateForm(instance=user)


        # other context data
        context['is_own_profile'] = (user == self.request.user)
        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)
        context['experiences'] = user.experiences.all()
        context['languages'] = user_languages
        context['nationalities'] = user_nationalities
        context['traits'] = personal_attributes
        context['section'] = section

        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if 'full_name_form' in request.POST:
            form = FullNameUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Full name updated successfully!")
            else:
                messages.error(request, "There was an error updating your full name.")

        elif 'salary_form' in request.POST:
            form = SalaryUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Salary preference updated successfully!")
            else:
                messages.error(request, "There was an error updating your salary preference.")

        elif 'location_form' in request.POST:
            form = LocationUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Current location updated successfully!")
            else:
                messages.error(request, "There was an error updating your current location.")

        return redirect('my_profile')
    
    
class RegisterView(generic.FormView, ContactFormMixin):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        try:
            user = form.save(commit=False)

            country = form.cleaned_data.get('location_country')
            city = form.cleaned_data.get('location_city')
            user.location = ", ".join(filter(None, [city, country]))

            user.save()

            user_name = form.cleaned_data.get('full_name')
            messages.success(self.request, f'Account has been created. Good luck, {user_name}!')
        except Exception as e:
            messages.error(self.request, f"An error occurred while creating your account: {e}")
            return self.form_invalid(form)
        
        return super().form_valid(form)
    

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                readable_field = field.capitalize().replace("_", " ")

                messages.error(self.request, f"{readable_field}: {error}")
        return super().form_invalid(form)
    

class ExperienceView(LoginRequiredMixin, FormView):
    form_class = ExperienceForm

    def form_valid(self, form):
        experience = form.save(commit=False)
        experience.user = self.request.user
        experience.save()
        messages.success(self.request, f'Experience added successfully!')
        return redirect('my_profile')


    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect('my_profile')
    
    
class WorkerTraitView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user

        data = json.loads(request.body)
        trait_id = data.get('trait_id')
        trait_score = data.get('trait_score')

        if not trait_id or not trait_score:
            return JsonResponse({'messages': ['Trait ID and score are required.']}, status=400)

        try:
            trait = Trait.objects.get(trait_id=trait_id) 
        except Trait.DoesNotExist:
            return JsonResponse({'messages': ['Trait not found.']}, status=404)

        try:
            _, created = WorkerTrait.objects.update_or_create(
                user=user,
                trait=trait,
                defaults={'trait_measure': trait_score},
            )
            if created:
                return JsonResponse({'messages': [f"Trait \"{trait.trait_name}\" added with score {trait_score}."]})
            else:
                return JsonResponse({'messages': [f"Trait \"{trait.trait_name}\" updated with score {trait_score}."]})
        except Exception as e:
            return JsonResponse({'messages': [f"An error occurred: {e}"]}, status=500)


class ContactView(FormView):
    template_name = "contact_form.html" 
    form_class = ContactForm
    success_url = reverse_lazy('index')  

    def form_valid(self, form):
        message = form.cleaned_data['contact']
        
        email = EmailMessage(
            subject="Contact Form Submission",
            body=message,
            from_email="anonym@user.com",
            to=[settings.EMAIL_HOST], 
        )
        try:
            email.send() 
            messages.success(self.request, "Your message has been sent successfully.")
        except Exception as e:
            messages.error(self.request, f"Failed to send the message: {e}")
        
        return super().form_valid(form)