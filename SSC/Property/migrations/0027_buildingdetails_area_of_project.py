# Generated by Django 5.1 on 2024-10-09 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0026_alter_buildingdetails_key_projects_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingdetails',
            name='area_of_project',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
