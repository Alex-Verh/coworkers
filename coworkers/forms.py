from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Experience


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


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'institution_name', 'description', 'start_year', 'end_year', 'type']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Experience Role'}),
            'institution_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Experience Institution'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 5, 'placeholder': 'Experience Description'}),
            'start_year': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Start Year', 'min': 1900, 'max': 2100}),
            'end_year': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'End Year*', 'min': 1900, 'max': 2100}),
            'type': forms.Select(attrs={'class': 'input'}),
        }

    def clean_start_year(self):
        start_year = self.cleaned_data.get('start_year')
        if not (1900 <= start_year <= 2100):
            raise forms.ValidationError("Start year must be between 1900 and 2100.")
        return start_year

    def clean_end_year(self):
        end_year = self.cleaned_data.get('end_year')
        start_year = self.cleaned_data.get('start_year')
        if end_year and not (1900 <= end_year <= 2100):
            raise forms.ValidationError("End year must be between 1900 and 2100.")
        if end_year and end_year < start_year:
            raise forms.ValidationError("End year cannot be earlier than start year.")
        return end_year