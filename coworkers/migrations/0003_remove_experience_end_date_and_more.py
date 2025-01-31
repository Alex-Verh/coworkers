# Generated by Django 5.0.6 on 2024-08-19 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0002_remove_workexperience_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='start_date',
        ),
        migrations.AddField(
            model_name='customuser',
            name='xing_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='end_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)]),
        ),
        migrations.AddField(
            model_name='experience',
            name='start_year',
            field=models.IntegerField(default=2014, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)]),
            preserve_default=False,
        ),
    ]
