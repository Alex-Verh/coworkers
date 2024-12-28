from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Experience
from datetime import date


@receiver(post_save, sender=Experience)
@receiver(post_delete, sender=Experience)
def update_user_experience(sender, instance, **kwargs):
    user = instance.user
    user.experience = calculate_total_experience(user)
    user.save()

def calculate_total_experience(user):
    work_experiences = user.experiences.filter(type='Work').order_by('start_year')

    if not work_experiences.exists():
        return 0

    first_experience = work_experiences.first()
    latest_experience = work_experiences.last()

    end_year = latest_experience.end_year or date.today().year
    total_experience = end_year - first_experience.start_year
    return total_experience
