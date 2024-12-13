# Generated by Django 3.2.25 on 2024-12-09 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='geo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.geo'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
