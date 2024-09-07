from rest_framework import serializers
from .models import ShortlistedProperty

class ShortlistedPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortlistedProperty
        fields = '__all__'
