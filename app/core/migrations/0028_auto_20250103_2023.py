# Generated by Django 3.2.25 on 2025-01-03 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20250103_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_pk',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_pk',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='todo',
            old_name='user_pk',
            new_name='user',
        ),
    ]
