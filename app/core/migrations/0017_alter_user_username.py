# Generated by Django 3.2.25 on 2024-12-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255),
        ),
    ]
