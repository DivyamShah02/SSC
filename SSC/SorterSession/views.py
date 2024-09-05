from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json

from Property.models import BuildingDetails, UnitDetails, Amenities
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer

from .sorting_logic import Sorter

# Create your views here.

class SorterViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        
        client_data = PropertyInquiry.objects.filter(id=data['id']).first()

        serializer = PropertyInquirySerializer(client_data)

        sorter = Sorter()

        updated_client_data = sorter.update_client_preferences(client_data=serializer.data)

        validated_property = sorter.get_pre_validated_property(update_client_data=updated_client_data)

        for property in validated_property:
            print(property.id)
            print(f'Property - {property.building_id}')
            print(f'bathroom - {property.no_of_attached_bathrooms}')
            print(f'bedroom - {property.unit_configuration}')
            print('----------------------------')

        print(len(validated_property))

        return Response({'Status':True})
