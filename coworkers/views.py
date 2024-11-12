from django.views import generic
from django.shortcuts import get_object_or_404
from .models import CustomUser, WorkerLanguage, WorkerNationality
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    template_name = "index.html"

    context_object_name = 'users'

    def get_queryset(self):
        """Return the last five published questions."""
        return CustomUser.objects.all()[:6]

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

        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)
        context['experiences'] = user.experiences.all()
        context['languages'] = user_languages
        context['nationalities'] = user_nationalities
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

