# Generated by Django 5.1.2 on 2024-12-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0009_workernationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='experience',
            field=models.IntegerField(default=0),
        ),
    ]
