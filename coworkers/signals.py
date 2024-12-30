from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Experience
from datetime import date
import random


@receiver(post_save, sender=Experience)
@receiver(post_delete, sender=Experience)
def update_user_experience(sender, instance, **kwargs):
    user = instance.user
    user.experience = calculate_total_experience(user)
    generate_user_description_task(user)
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


def generate_user_description_task(user):
    work_experiences = user.experiences.filter(type='Work').order_by('start_year')

    if not work_experiences:
        user.description = (
            f"{user.full_name} is an eager, talented worker seeking a position at multiple potential companies. "
            "They have not indicated any work experience records but can still successfully perform their job."
        )
    else:
        experience_list = []
        
        for exp in work_experiences:
            end_year = exp.end_year if exp.end_year else "present"
            experience = f"{exp.position} at {exp.institution_name} ({exp.start_year} - {end_year})"
            experience_list.append(experience)
        
        experience_summary = " | ".join(experience_list)

        # List of possible last sentences
        last_sentences = [
            "They have consistently excelled in every role, adapting to new challenges with ease.",
            "Their ability to thrive in diverse work environments speaks to their versatility and expertise.",
            "With a proven track record, they’ve shown exceptional adaptability and problem-solving skills.",
            "They bring a unique blend of skills, demonstrated through their success across multiple roles.",
            "Throughout their career, they have shown a strong ability to meet challenges head-on and deliver results.",
            "Their work history highlights their remarkable versatility and capacity to excel under pressure.",
            "They have repeatedly proven their ability to adjust to new roles and responsibilities with success.",
            "In each position, they’ve exhibited strong leadership and adaptability to meet organizational goals.",
            "Their diverse experience shows a commitment to continuous growth and excellence in every role.",
            "They’ve consistently adapted to different work environments, making valuable contributions along the way."
        ]

        random_last_sentence = random.choice(last_sentences)


        user.description = (
            f"{user.full_name} has a strong background in various roles, including: {experience_summary}. "
            f"{random_last_sentence}"

        )
    
    user.save()