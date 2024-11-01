from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("profile", views.ProfileView.as_view(), name="my_profile"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="user_profile"),
    path("register", views.RegisterView.as_view(), name="register"),
]
