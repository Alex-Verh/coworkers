from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("profile", views.ProfileView.as_view(), name="my_profile"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="user_profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='logout.html'), name='logout')
]
