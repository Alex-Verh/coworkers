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
