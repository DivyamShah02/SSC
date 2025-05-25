from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.

class ShortlistedProperty(models.Model):
    client_id = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    number = models.CharField(null=True, blank=True, max_length=15)
    properties = models.TextField(null=True, blank=True)
    selected_properties = models.TextField(null=True, blank=True, default='')
    hidden_properties = models.TextField(null=True, blank=True, default='')
    visit_details = models.TextField(null=True, blank=True, default='')
    start_visit_time_date = models.CharField(null=True, blank=True, default='', max_length=255)
    visit_start_coords = models.CharField(null=True, blank=True, default='', max_length=255)
    visit_start_location = models.CharField(null=True, blank=True, default='', max_length=255)
    visist_finalize = models.BooleanField(default=False)
    feedback = models.TextField(null=True, blank=True, default='')
    visit_plan_pdf = models.FileField(upload_to='visit_plan', storage=S3Boto3Storage(), null=True, blank=True)

