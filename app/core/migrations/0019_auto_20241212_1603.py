# Generated by Django 3.2.25 on 2024-12-12 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20241212_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='user_pk',
            new_name='userId',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='album_pk',
            new_name='albumId',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='user_pk',
            new_name='user',
        ),
    ]
