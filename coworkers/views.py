from django.views import generic
from django.shortcuts import get_object_or_404
from .models import CustomUser, WorkerLanguage, WorkerNationality, Trait, WorkerTrait
from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_section'] = CustomUser.objects.all()[:6]  # first section
        context['users_paginated'] = CustomUser.objects.all()  # second section
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
    

class ProfileView(LoginRequiredMixin, generic.DetailView):
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
    

class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        user = form.save(commit=False)

        country = form.cleaned_data.get('location_country')
        city = form.cleaned_data.get('location_city')

        user.location = f"{city}, {country}" if city and country else city or country
        user.save()

        user_name = form.cleaned_data.get('full_name')
        messages.success(self.request, f'Account has been created. Good luck, {user_name}!')
        return super().form_valid(form)

