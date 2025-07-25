from django.contrib import admin
from .models import BunglowDetails, BunglowUnitDetails, BunglowAmenities

class AdminBunglowDetails(admin.ModelAdmin):
    list_display = ('bunglow_id', 'project_name', 'group_name', 'year_of_establishment', 'name', 'number', 'type_of_apartments')
    list_filter = ('group_name', 'area_of_project', 'sample_house', 'bunglow_added_by')
    search_fields = ('project_name', 'bunglow_id', 'area_of_project')
admin.site.register(BunglowDetails, AdminBunglowDetails)

class AdminBunglowUnitDetails(admin.ModelAdmin):
    list_display = ('project_name', 'group_name', 'size_of_unit', 'bunglow_id', 'unit_configuration', 'unit_type')
    search_fields = ('project_name', 'group_name', 'size_of_unit', 'bunglow_id', 'unit_configuration', 'unit_type')
    list_filter = ('unit_configuration', 'unit_type')

admin.site.register(BunglowUnitDetails, AdminBunglowUnitDetails)

class AdminBunglowAmenities(admin.ModelAdmin):
    list_display = ('bunglow_id',)
admin.site.register(BunglowAmenities, AdminBunglowAmenities)

