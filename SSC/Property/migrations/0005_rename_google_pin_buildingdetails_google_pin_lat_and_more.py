# Generated by Django 5.1 on 2024-09-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0004_unitdetails_google_pin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buildingdetails',
            old_name='google_pin',
            new_name='google_pin_lat',
        ),
        migrations.RenameField(
            model_name='unitdetails',
            old_name='google_pin',
            new_name='google_pin_lat',
        ),
        migrations.AddField(
            model_name='buildingdetails',
            name='google_pin_lng',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='unitdetails',
            name='google_pin_lng',
            field=models.CharField(default='', max_length=255),
        ),
    ]