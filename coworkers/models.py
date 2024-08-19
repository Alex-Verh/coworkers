# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email_address, first_name, last_name, password=None, **extra_fields
    ):
        if not email_address:
            raise ValueError("The Email field must be set")
        email_address = self.normalize_email(email_address)
        user = self.model(
            email_address=email_address,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email_address, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email_address, first_name, last_name, password, **extra_fields
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
    email_address = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
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

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=EXPERIENCE_TYPE)

    def __str__(self):
        return self.job_position


class WorkerTrait(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    trait_measure = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "trait")

    def __str__(self):
        return f"{self.user} - {self.trait} - {self.trait_measure}"
