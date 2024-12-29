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

    total_experience = 0
    
    current_start_year = work_experiences.first().start_year
    current_end_year = work_experiences.first().end_year or date.today().year

    for experience in work_experiences[1:]:
        end_year = experience.end_year if experience.end_year else date.today().year

        if experience.start_year <= current_end_year:
            current_end_year = max(current_end_year, end_year)
        else:
            total_experience += current_end_year - current_start_year
            current_start_year = experience.start_year
            current_end_year = end_year

    total_experience += current_end_year - current_start_year

    return total_experience