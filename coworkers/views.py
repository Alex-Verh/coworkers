from django.views import generic
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


class IndexView(generic.ListView):
    template_name = "index.html"

    context_object_name = 'users'

    def get_queryset(self):
        """Return the last five published questions."""
        return CustomUser.objects.all()[:6]

class ProfileView(generic.DetailView):
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
        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)
        context['experiences'] = user.experiences.all()
        return context


class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account has been created. Good luck, {username}!')
        return super().form_valid(form)

