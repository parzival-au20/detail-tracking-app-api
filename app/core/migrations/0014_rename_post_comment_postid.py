# Generated by Django 3.2.25 on 2024-12-10 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_album_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='postId',
        ),
    ]
