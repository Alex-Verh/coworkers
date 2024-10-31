from django.views import generic
from django.shortcuts import get_object_or_404
from .models import CustomUser


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


class RegisterView(generic.ListView):
    template_name = "register.html"

    def get_queryset(self):
        return 