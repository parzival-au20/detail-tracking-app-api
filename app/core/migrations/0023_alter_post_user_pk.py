# Generated by Django 3.2.25 on 2025-01-02 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_rename_user_todo_user_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_pk',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
