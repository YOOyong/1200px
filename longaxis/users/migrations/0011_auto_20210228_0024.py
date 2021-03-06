# Generated by Django 3.1.1 on 2021-02-28 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20210228_0019'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='follow_from',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='following',
            new_name='follow_to',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follow_from', 'follow_to'), name='unique_follow'),
        ),
    ]
