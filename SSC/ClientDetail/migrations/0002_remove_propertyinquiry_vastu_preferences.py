# Generated by Django 5.1 on 2024-10-09 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClientDetail', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyinquiry',
            name='vastu_preferences',
        ),
    ]
