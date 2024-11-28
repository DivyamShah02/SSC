from django.contrib import admin
from .models import BuildingDetails, UnitDetails, Amenities

class AdminBuildingDetails(admin.ModelAdmin):
    list_display = ('building_id', 'project_name', 'group_name', 'year_of_establishment', 'name', 'number', 'type_of_apartments')
    list_filter = ('group_name', 'area_of_project')
    search_fields = ('project_name', 'building_id', 'area_of_project')
admin.site.register(BuildingDetails, AdminBuildingDetails)

class AdminUnitDetails(admin.ModelAdmin):
    list_display = ('project_name', 'group_name', 'size_of_unit', 'building_id', 'unit_configuration', 'unit_type')
    search_fields = ('project_name', 'group_name', 'size_of_unit', 'building_id', 'unit_configuration', 'unit_type')
    list_filter = ('unit_configuration', 'unit_type')

admin.site.register(UnitDetails, AdminUnitDetails)

class AdminAmenities(admin.ModelAdmin):
    list_display = ('building_id',)
admin.site.register(Amenities, AdminAmenities)

