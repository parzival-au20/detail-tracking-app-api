# Generated by Django 3.2.25 on 2024-12-10 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20241210_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]