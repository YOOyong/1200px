# Generated by Django 3.1.1 on 2021-03-04 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='gallery.photo'),
        ),
    ]