from django.contrib import admin
from .models import BuildingDetails, UnitDetails, Amenities

class AdminBuildingDetails(admin.ModelAdmin):
    list_display = ('building_id', 'group_name', 'year_of_establishment', 'name', 'number', 'type_of_apartments')
admin.site.register(BuildingDetails, AdminBuildingDetails)

class AdminUnitDetails(admin.ModelAdmin):
    list_display = ('building_id', 'unit_configuration', 'unit_type', 'no_of_units_per_floor')
admin.site.register(UnitDetails, AdminUnitDetails)

class AdminAmenities(admin.ModelAdmin):
    list_display = ('building_id',)
admin.site.register(Amenities, AdminAmenities)

