from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Experience


class CustomUserCreationForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        error_messages={
            'invalid': "Enter a valid full name.",
            'required': "Full name is required.",
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

class PfpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and not picture.name.endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError('Only JPG, JPEG, and PNG formats are accepted.')
        return picture

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['position', 'institution_name', 'description', 'start_year', 'end_year', 'type']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Role/Faculty'}),
            'institution_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Institution Name'}),
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
    

class ContactForm(forms.Form):
    contact = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'textarea'}),
        label="Message",
        max_length=2000,
        required=True
    )


class FullNameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'input', 'placeholder': "Full Name"}),
        }
        labels = {
            'full_name': 'Full Name',
        }


class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['location']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': "City, Country"}),
        }
        labels = {
            'location': 'Current Location',
        }


class SalaryUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['salary_minimum', 'salary_maximum']
        labels = {
            'salary_minimum': 'Minimum Salary',
            'salary_maximum': 'Maximum Salary',
        }
        widgets = {
            'salary_minimum': forms.NumberInput(attrs={'class': 'input text-center', 'step': '0.01', 'placeholder': 'Minimum', 'min': 0, 'max': 10000000}),
            'salary_maximum': forms.NumberInput(attrs={'class': 'input text-center', 'step': '0.01', 'placeholder': 'Maximum', 'min': 0, 'max': 10000000}),
        }

    def clean(self):
        cleaned_data = super().clean()
        salary_minimum = cleaned_data.get('salary_minimum')
        salary_maximum = cleaned_data.get('salary_maximum')

        if salary_minimum is not None and salary_maximum is not None:
            if salary_minimum > salary_maximum:
                raise forms.ValidationError(
                    "Minimum salary cannot be greater than maximum salary."
                )
            elif salary_maximum < 0 or salary_minimum < 0:
                raise forms.ValidationError(
                    "Salary value cannot be less than 0."
                )
            
        return cleaned_data