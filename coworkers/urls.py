from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("profile", views.ProfileView.as_view(), name="my_profile"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="user_profile"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    path('worker-trait/', views.WorkerTraitView.as_view(), name='worker-trait'),
    path('contact-us/', views.ContactView.as_view(), name='contact-us'),
    path('languages/', views.LanguageView.as_view(), name='language'),
    path('languages/own/', views.LanguageView.as_view(), name='own_language'),
    path('nationalities/', views.NationalityView.as_view(), name='nationality'),
    path('nationalities/own/', views.NationalityView.as_view(), name='own_nationality'),
]
