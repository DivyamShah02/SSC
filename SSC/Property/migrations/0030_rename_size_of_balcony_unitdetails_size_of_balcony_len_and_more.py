# Generated by Django 5.1 on 2024-10-17 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0029_buildingdetails_alternate_number_country_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unitdetails',
            old_name='size_of_balcony',
            new_name='size_of_balcony_len',
        ),
        migrations.RenameField(
            model_name='unitdetails',
            old_name='size_of_kitchen',
            new_name='size_of_balcony_wid',
        ),
        migrations.RenameField(
            model_name='unitdetails',
            old_name='size_of_master_bedroom',
            new_name='size_of_kitchen_len',
        ),
        migrations.RenameField(
            model_name='unitdetails',
            old_name='size_of_private_terrace',
            new_name='size_of_private_terrace_len',
        ),
        migrations.AddField(
            model_name='unitdetails',
            name='size_of_kitchen_wid',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='unitdetails',
            name='size_of_master_bedroom_len',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='unitdetails',
            name='size_of_master_bedroom_wid',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='unitdetails',
            name='size_of_private_terrace_wid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
