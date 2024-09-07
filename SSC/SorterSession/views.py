from Property.models import BuildingDetails, UnitDetails, Amenities
from Property.serializers import UnitDetailsSerializer, BuildingDetailsSerializer
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer
from .models import ShortlistedProperty
from .serializers import ShortlistedPropertySerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
import json

from .sorting_logic import Sorter


class SorterViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            data = request.data
            inquiry_id = data.get('id')

            if not inquiry_id:
                return Response({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            client_data_obj = get_object_or_404(PropertyInquiry, id=inquiry_id)
            client_data = PropertyInquirySerializer(client_data_obj).data

            sorter = Sorter()

            updated_client_data = sorter.update_client_preferences(client_data=client_data)
            validated_properties = sorter.get_pre_validated_property(updated_client_data=updated_client_data)
            sorted_data = sorter.generate_property_list(updated_client_data=updated_client_data, validated_properties=validated_properties)

            session_already_exists = ShortlistedProperty.objects.filter(client_id=inquiry_id).first()
            if session_already_exists:
                edit_session = ShortlistedProperty.objects.get(client_id=inquiry_id)

                edit_session.number = client_data.get('number','')
                edit_session.properties = sorted_data

                edit_session.save()
                session_id = edit_session.id
                
            else:
                 new_session = ShortlistedProperty(
                      client_id=inquiry_id,
                      number=client_data.get('number',''),
                      properties=sorted_data
                 )

                 new_session.save()
                 session_id = new_session.id

            return Response({
                'status': True,
                'session_id': session_id
            }, status=status.HTTP_200_OK)

        except PropertyInquiry.DoesNotExist:
            return Response({'status': False, 'error': 'Property Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyViewset(viewsets.ViewSet):
    def list(self, request):
        session_id = request.GET.get('id')

        session_data_obj = get_object_or_404(ShortlistedProperty, id=session_id)
        session_data = ShortlistedPropertySerializer(session_data_obj).data

        properties_data = session_data.get('properties', '').replace("'", '"')
        properties_data = json.loads(properties_data)

        all_properties = []
        for property in properties_data:
            unit_id = property['unit_id']
            unit_data_obj = get_object_or_404(UnitDetails, id=unit_id)
            unit_data = UnitDetailsSerializer(unit_data_obj).data

            building_data_obj = get_object_or_404(BuildingDetails, building_id=unit_data.get('building_id', 0))
            building_data = BuildingDetailsSerializer(building_data_obj).data

            property_details={
                'unit_id': unit_id,
                'unit_details': unit_data,
                'building_id': unit_data.get('building_id', 0),
                'building_details':building_data,
                'score': property['score']
            }

            all_properties.append(property_details)

        return Response({'success':True, 'all_properties':all_properties})


    def create(self, request):
        data = request.data
        session_id = data.get('id')

        session_data_obj = get_object_or_404(ShortlistedProperty, id=session_id)
        session_data = ShortlistedPropertySerializer(session_data_obj).data

        properties_data = session_data.get('properties', '').replace("'", '"')
        properties_data = json.loads(properties_data)

        all_properties = []
        for property in properties_data:
            unit_id = property['unit_id']
            unit_data_obj = get_object_or_404(UnitDetails, id=unit_id)
            unit_data = UnitDetailsSerializer(unit_data_obj).data

            building_data_obj = get_object_or_404(BuildingDetails, building_id=unit_data.get('building_id', 0))
            building_data = BuildingDetailsSerializer(building_data_obj).data

            property_details={
                'unit_id': unit_id,
                'unit_details': unit_data,
                'building_id': unit_data.get('building_id', 0),
                'building_details':building_data,
                'score': property['score']
            }

            all_properties.append(property_details)

        return Response({'success':True, 'all_properties':all_properties})

