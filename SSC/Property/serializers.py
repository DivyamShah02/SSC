from rest_framework import serializers
from .models import UnitDetails, BuildingDetails, Amenities

class UnitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitDetails
        fields = '__all__'

class BuildingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDetails
        fields = '__all__'

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'
