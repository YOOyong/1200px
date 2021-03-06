# Generated by Django 3.1.1 on 2021-02-26 15:46

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/default_profile.jpg', null=True, upload_to=users.models.user_directory_path),
        ),
    ]
