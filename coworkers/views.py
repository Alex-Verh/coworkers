from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser, WorkerLanguage, WorkerNationality, Trait, WorkerTrait
from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ExperienceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.edit import FormView, View
from .mixins import ExperienceFormMixin
import json


class IndexView(generic.ListView):
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
    

class ProfileView(LoginRequiredMixin, ExperienceFormMixin, generic.DetailView):
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

        context['is_own_profile'] = (user == self.request.user)
        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)
        context['experiences'] = user.experiences.all()
        context['languages'] = user_languages
        context['nationalities'] = user_nationalities
        context['traits'] = personal_attributes
        context['section'] = section

        return context
    

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
    

class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        user = form.save(commit=False)

        country = form.cleaned_data.get('location_country')
        city = form.cleaned_data.get('location_city')

        user.location = ", ".join(filter(None, [city, country]))
        user.save()

        user_name = form.cleaned_data.get('full_name')
        messages.success(self.request, f'Account has been created. Good luck, {user_name}!')
        return super().form_valid(form)

