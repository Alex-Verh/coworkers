# Generated by Django 5.1.2 on 2024-11-03 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0005_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='email_address',
            new_name='email',
        ),
    ]
