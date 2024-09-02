from rest_framework import serializers
from .models import PropertyInquiry

class PropertyInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInquiry
        fields = '__all__'
