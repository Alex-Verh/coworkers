from django.contrib import admin

from .models import (
    CustomUser,
    Experience,
    Language,
    Nationality,
    Trait,
    WorkerTrait,
)

# Register your models here.
admin.site.register(
    (
        Nationality,
        Language,
        Trait,
        CustomUser,
        Experience,
        WorkerTrait,
    )
)
