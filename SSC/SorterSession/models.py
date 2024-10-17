from django.db import models

# Create your models here.

class ShortlistedProperty(models.Model):
    client_id = models.CharField(max_length=255)
    number = models.CharField(null=True, blank=True, max_length=15)
    properties = models.TextField(null=True, blank=True)
