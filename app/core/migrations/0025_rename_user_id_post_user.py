# Generated by Django 3.2.25 on 2025-01-03 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_rename_user_pk_post_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
    ]