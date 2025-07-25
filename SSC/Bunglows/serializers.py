from rest_framework import serializers
from .models import BunglowUnitDetails, BunglowDetails, BunglowAmenities

class BunglowUnitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunglowUnitDetails
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'type_of_parking' in representation:
            type_of_parking = str(representation['type_of_parking']).split(', ')
            representation['type_of_parking'] = type_of_parking
        return representation


class BunglowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunglowDetails
        fields = '__all__'

class BunglowAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunglowAmenities
        fields = '__all__'
