# Generated by Django 5.1 on 2024-09-30 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0008_alter_buildingdetails_spiritual_or_religious_attraction'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingdetails',
            name='rera_approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
