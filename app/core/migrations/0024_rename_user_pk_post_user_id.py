# Generated by Django 3.2.25 on 2025-01-03 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_post_user_pk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_pk',
            new_name='user_id',
        ),
    ]
