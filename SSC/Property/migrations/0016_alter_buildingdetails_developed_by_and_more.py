# Generated by Django 5.1 on 2024-10-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0015_alter_buildingdetails_age_of_property_by_developer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingdetails',
            name='developed_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='location_of_project',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='project_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='project_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
