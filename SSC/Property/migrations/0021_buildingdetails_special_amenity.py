# Generated by Django 5.1 on 2024-10-05 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0020_buildingdetails_brochure_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingdetails',
            name='special_amenity',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
