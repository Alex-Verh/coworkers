from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Experience
from datetime import date
import re
from urllib.parse import urlparse
from PIL import Image


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

    birth_date = None 
    location = None

    profile_picture = forms.ImageField(
        required=False,
        label="Profile Picture",
        error_messages={
            'invalid': "Upload a valid image. The file must be a .jpg, .jpeg, or .png.",
        }
    )

    def clean(self):
        cleaned_data = super().clean()

        birth_day = cleaned_data.get("birth_day")
        birth_month = cleaned_data.get("birth_month")
        birth_year = cleaned_data.get("birth_year")

        if birth_day and birth_month and birth_year:
            try:
                self.birth_date = date(birth_year, birth_month, birth_day)
            except ValueError:
                raise ValidationError({"birth_day": "Invalid birth date. Please check the day, month, and year."})
        else:
            raise forms.ValidationError({"birth_day": "Birth day, month, and year are required to compute the birth date."})

                
        country = cleaned_data.get('location_country')
        city = cleaned_data.get('location_city')

        if country and city:
            try:
                self.location = ", ".join(filter(None, [city, country]))
            except ValueError:
                raise ValidationError({"location": "Invalid location or city address."})
        else:
            raise ValidationError({"location": "City and country locations are required to compute your location"})
    

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        
        return password
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and not picture.name.endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError('Only JPG, JPEG, and PNG formats are accepted.')
        
        # Validate image content using Pillow
        if picture:
            try:
                img = Image.open(picture)
                img.verify()  # Validate the file is a valid image
            except Exception as e:
                raise forms.ValidationError("Uploaded file is not a valid image.")
            
        if picture and picture.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size must not exceed 10MB.')
        return picture
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"]) 
        user.birth_date = self.birth_date 
        user.location = self.location 

        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("full_name", "email", "password", "full_name", "profile_picture", "location_country", "location_city", "birth_day", "birth_month", "birth_year", "location", "birth_date", "findus")

class PfpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        # Validate image content using Pillow
        try:
            img = Image.open(picture)
            img.verify()  # Validate the file is a valid image
        except Exception as e:
            raise forms.ValidationError("Uploaded file is not a valid image.")

        if picture and not picture.name.endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError('Only JPG, JPEG, and PNG formats are accepted.')
        
        if picture and picture.size > 10 * 1024 * 1024:
            raise forms.ValidationError('File size must not exceed 10MB.')
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

class LinksUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['linkedin_link', 'xing_link', 'personal_link']
        widgets = {
            'linkedin_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'https://www.linkedin.com/in/'}),
            'xing_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'https://www.xing.com/profile/'}),
            'personal_link': forms.TextInput(attrs={'class': 'input', 'placeholder': 'https://personal.com/'}),
        }

    def clean_linkedin_link(self):
        linkedin_link = self.cleaned_data.get('linkedin_link')
        if linkedin_link and not re.match(r'https://www\.linkedin\.com/in/[\w-]+', linkedin_link):
            raise ValidationError("Please provide a valid LinkedIn URL.")
        return linkedin_link

    def clean_xing_link(self):
        xing_link = self.cleaned_data.get('xing_link')
        if xing_link and not re.match(r'https://www\.xing\.com/profile/[\w-]+', xing_link):
            raise ValidationError("Please provide a valid Xing URL.")
        return xing_link
    
    def clean_personal_link(self):
        personal_link = self.cleaned_data.get('personal_link')
        
        if personal_link:
            try:
                parsed_url = urlparse(personal_link)
                if not parsed_url.scheme or not parsed_url.netloc:
                    raise ValidationError("Invalid URL format.")
                
                # Check the domain of the URL to ensure it's from a trusted source
                # allowed_domains = ['github.com', 'youtube.com']
                # if parsed_url.netloc not in allowed_domains:
                #     raise ValidationError("Personal URL must be from an allowed domain (e.g., github.com, youtube.com).")
                
            except ValueError:
                raise ValidationError("Please provide a valid personal link URL.")

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