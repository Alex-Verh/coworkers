from django.contrib import admin

from .models import (
    CustomUser,
    EducationExperience,
    Language,
    Nationality,
    Rank,
    Trait,
    WorkerTrait,
    WorkExperience,
)

# Register your models here.
admin.site.register(
    (
        Rank,
        Nationality,
        Language,
        Trait,
        CustomUser,
        EducationExperience,
        WorkExperience,
        WorkerTrait,
    )
)
