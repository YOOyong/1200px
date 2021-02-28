# Generated by Django 3.1.1 on 2021-02-28 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210228_1724'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follow_to',
            new_name='following_user',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follow_from',
            new_name='user',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following_user'), name='unique_follow'),
        ),
    ]
