# Generated by Django 4.2.4 on 2024-04-30 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0010_user_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='image_url',
        ),
    ]