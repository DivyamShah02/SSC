# Generated by Django 5.1 on 2024-09-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0005_rename_google_pin_buildingdetails_google_pin_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitdetails',
            name='location_of_project',
            field=models.TextField(default=''),
        ),
    ]
