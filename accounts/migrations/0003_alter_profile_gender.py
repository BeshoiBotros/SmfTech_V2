# Generated by Django 5.0.6 on 2024-06-20 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=255, null=True),
        ),
    ]
