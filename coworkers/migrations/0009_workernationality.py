# Generated by Django 5.1.2 on 2024-11-12 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coworkers', '0008_alter_workerlanguage_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerNationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coworkers.nationality')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'nationality')},
            },
        ),
    ]
