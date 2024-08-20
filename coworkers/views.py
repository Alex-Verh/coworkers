from django.shortcuts import render
from django.views import generic

from .models import CustomUser


class IndexView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return the last five published questions."""
        return CustomUser.objects.all()[:20]


class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = "profile.html"

    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)
        context['experiences'] = user.experiences.all()
        return context
