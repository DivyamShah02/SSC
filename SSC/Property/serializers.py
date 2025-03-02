from rest_framework import serializers
from .models import UnitDetails, BuildingDetails, Amenities

class UnitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitDetails
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'type_of_parking' in representation:
            type_of_parking = str(representation['type_of_parking']).split(', ')
            representation['type_of_parking'] = type_of_parking
        return representation


class BuildingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDetails
        fields = '__all__'

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'
