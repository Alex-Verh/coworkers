# Generated by Django 5.1.4 on 2025-01-01 19:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0011_customuser_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='portfolio_link',
        ),
        migrations.AlterField(
            model_name='experience',
            name='end_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)]),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)]),
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]
