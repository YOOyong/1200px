# Generated by Django 3.1.1 on 2021-02-22 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='img_height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='img_width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]