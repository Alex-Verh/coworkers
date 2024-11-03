import os
import django
from django.core.management.base import BaseCommand
import datetime

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Setup Django
django.setup()

# Import your models after setting up Django
from coworkers.models import CustomUser, Rank, Nationality, Language, Trait, Experience, WorkerTrait
from faker import Faker
import random

# Create Faker instance
fake = Faker()

class Command(BaseCommand):
    help = "Populates the database with fake data"

    def handle(self, *args, **kwargs):
        try:

            self.stdout.write(self.style.SUCCESS("Starting the populate_db command..."))

            # Generate Ranks
            ranks = [Rank.objects.create(rank_symbol=f"R{n}", rank_name=f"Rank {n}") for n in range(1, 4)]
            self.stdout.write(self.style.SUCCESS("Ranks created"))

            # Generate Nationalities
            nationalities = [Nationality.objects.create(nationality_name=fake.country()) for _ in range(5)]
            self.stdout.write(self.style.SUCCESS("Nationalities created"))

            # Generate Languages
            languages = [Language.objects.create(language_name=fake.language_name()) for _ in range(5)]
            self.stdout.write(self.style.SUCCESS("Languages created"))

            # Generate Traits
            traits = [
                Trait.objects.create(trait_name=fake.word(), trait_description=fake.text())
                for _ in range(10)
            ]
            self.stdout.write(self.style.SUCCESS("Traits created"))

            # Generate Users
            for _ in range(20):
                user = CustomUser.objects.create_user(
                    email=fake.email(),
                    full_name=fake.first_name() + " " + fake.last_name(),
                    password="password123",
                    birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
                    profile_picture=None,
                    location=fake.city(),
                    salary_minimum=random.uniform(30000, 50000),
                    salary_maximum=random.uniform(60000, 120000),
                    linkedin_link=fake.url(),
                    xing_link=fake.url(),
                    personal_link=fake.url(),
                    portfolio_link=fake.url(),
                    rank=random.choice(ranks),
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.first_name} {user.last_name}"))

                user.nationalities.set(random.sample(nationalities, k=2))
                user.languages.set(random.sample(languages, k=2))
                
                # Generate Experiences for each user
                for _ in range(random.randint(1, 5)):
                    start_year = random.randint(2000, 2015)
                    end_year = random.choice([None, random.randint(start_year + 1, datetime.datetime.now().year)])
                    Experience.objects.create(
                        institution_name=fake.company(),
                        position=fake.job(),
                        description=fake.paragraph(),
                        start_year=start_year,
                        end_year=end_year,
                        user=user,
                        type=random.choice(["Work", "Education"]),
                    )
                    self.stdout.write(self.style.SUCCESS("Experience created"))

                # Generate WorkerTraits for each user
                for trait in random.sample(traits, k=3):
                    WorkerTrait.objects.create(
                        user=user,
                        trait=trait,
                        trait_measure=random.randint(1, 10),
                    )
                    self.stdout.write(self.style.SUCCESS("WorkerTrait created"))

            self.stdout.write(self.style.SUCCESS("Successfully populated the database with fake data"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
