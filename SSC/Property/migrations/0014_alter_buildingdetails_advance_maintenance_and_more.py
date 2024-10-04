# Generated by Django 5.1 on 2024-10-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Property', '0013_rename_age_of_property_developer_buildingdetails_age_of_property_by_developer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingdetails',
            name='advance_maintenance',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='development_charges',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='gst_applicable',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='head_image',
            field=models.ImageField(blank=True, null=True, upload_to='property'),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='maintenance_deposit',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='plc_corner',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='plc_garden',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='plc_others',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='plc_road_facing',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='sale_deed_value',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='sale_deed_value_max',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='sale_deed_value_min',
            field=models.TextField(blank=True, default=0, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='sec_image_1',
            field=models.ImageField(blank=True, null=True, upload_to='property'),
        ),
        migrations.AlterField(
            model_name='buildingdetails',
            name='sec_image_2',
            field=models.ImageField(blank=True, null=True, upload_to='property'),
        ),
    ]
