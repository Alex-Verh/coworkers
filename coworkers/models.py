# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, date


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, full_name, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, full_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email, full_name, password, **extra_fields
        )


class Rank(models.Model):
    rank_id = models.AutoField(primary_key=True)
    rank_symbol = models.CharField(max_length=50)
    rank_name = models.CharField(max_length=100)

    def __str__(self):
        return self.rank_name


class Nationality(models.Model):
    nationality_id = models.AutoField(primary_key=True)
    nationality_name = models.CharField(max_length=100)

    def __str__(self):
        return self.nationality_name


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=100)

    def __str__(self):
        return self.language_name


class Trait(models.Model):
    trait_id = models.AutoField(primary_key=True)
    trait_name = models.CharField(max_length=100)
    trait_description = models.TextField()

    def __str__(self):
        return self.trait_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    salary_minimum = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    salary_maximum = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    linkedin_link = models.URLField(null=True, blank=True)
    xing_link = models.URLField(null=True, blank=True)
    personal_link = models.URLField(null=True, blank=True)
    portfolio_link = models.URLField(null=True, blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, null=True, blank=True)
    nationalities = models.ManyToManyField(Nationality, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    traits = models.ManyToManyField(Trait, through="WorkerTrait", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "birth_date", "location"]

    def __str__(self):
        return f"{self.full_name}"
    
    @property
    def age(self):
        if self.birth_date is None:
            return "N/A"
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    @property
    def position(self):
        work_experiences = self.experiences.filter(type='Work').order_by('start_year')

        if not work_experiences.exists():
            return "Job Seeker"

        latest_experience = work_experiences.last()
        lastest_position = latest_experience.position

        return lastest_position
    
    @property
    def experience(self):
        work_experiences = self.experiences.filter(type='Work').order_by('start_year')
        
        if not work_experiences.exists():
            return 0

        first_experience = work_experiences.first()
        latest_experience = work_experiences.last()

        end_year = latest_experience.end_year or date.today().year

        total_experience = end_year - first_experience.start_year
        return total_experience
    
    def formatted_salary(self, salary):
        if salary is None:
            return "N/A"
        elif salary >= 1000:
            return f"{int(salary // 1000)}k"
        return f"{salary:.0f}" if salary.is_integer() else f"{salary:.2f}"


class Experience(models.Model):
    EXPERIENCE_TYPE = [
        ('Education', 'Education'),
        ('Work', 'Work'),
    ]
    CURRENT_YEAR = datetime.now().year


    experience_id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField()

    start_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(CURRENT_YEAR)
        ]
    )
    end_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(CURRENT_YEAR)
        ], null=True, blank=True
    )
    user = models.ForeignKey(CustomUser, related_name='experiences', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=EXPERIENCE_TYPE)

    def __str__(self):
        return self.position


class WorkerLanguage(models.Model):
    KNOWLEDGE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Professional', 'Professional'),
        ('Native', 'Native'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    language_knowledge = models.CharField(max_length=50, choices=KNOWLEDGE_CHOICES)

    class Meta:
        unique_together = ("user", "language")

    def __str__(self):
        return f"{self.user} - {self.language} - {self.language_knowledge}"
    

class WorkerNationality(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "nationality")

    def __str__(self):
        return f"{self.user} - {self.nationality}"
    

class WorkerTrait(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    trait_measure = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "trait")

    def __str__(self):
        return f"{self.user} - {self.trait} - {self.trait_measure}"
