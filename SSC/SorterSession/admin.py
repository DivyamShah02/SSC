from django.contrib import admin
from .models import ShortlistedProperty
# Register your models here.

class AdminShortlistedProperty(admin.ModelAdmin):
    list_display = ('name', 'client_id', 'number', 'properties')
admin.site.register(ShortlistedProperty, AdminShortlistedProperty)
