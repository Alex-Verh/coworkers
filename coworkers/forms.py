from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        error_messages={
            'invalid': "Enter a valid email address.",
            'required': "Email is required.",
        }
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': "Enter a valid email address.",
            'required': "Email is required.",
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Password cannot be empty.",
        }
    )

    location_country = forms.CharField(required=True, label="Current Location, Country")
    location_city = forms.CharField(required=True, label="Current Location, City")
    birth_day = forms.IntegerField(required=True, label="Birth Day", min_value=1, max_value=31)
    birth_month = forms.IntegerField(required=True, label="Birth Month", min_value=1, max_value=12)
    birth_year = forms.IntegerField(required=True, label="Birth Year", min_value=1900, max_value=2100)
    findus = forms.CharField(required=False, widget=forms.Textarea, label="How did you find about us?")


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("full_name", "email", "password", "full_name", "location_country", "location_city", "birth_day", "birth_month", "birth_year", "findus")

