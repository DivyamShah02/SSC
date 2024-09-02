from django.contrib import admin
from .models import PropertyInquiry


class AdminPropertyInquiry(admin.ModelAdmin):
    list_display = ('name', 'number', 'whatsapp', 'email', 'profession')
admin.site.register(PropertyInquiry, AdminPropertyInquiry)
