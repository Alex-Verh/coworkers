from django.contrib import admin

from .models import (
    CustomUser,
    Experience,
    Language,
    Nationality,
    Rank,
    Trait,
    WorkerTrait,
)

# Register your models here.
admin.site.register(
    (
        Rank,
        Nationality,
        Language,
        Trait,
        CustomUser,
        Experience,
        WorkerTrait,
    )
)
