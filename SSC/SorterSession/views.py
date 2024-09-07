from Property.models import BuildingDetails, UnitDetails, Amenities
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .sorting_logic import Sorter


class SorterViewSet(viewsets.ViewSet):
    def create(self, request):
        # try:
            data = request.data
            inquiry_id = data.get('id')

            if not inquiry_id:
                return Response({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            client_data = get_object_or_404(PropertyInquiry, id=inquiry_id)
            serializer = PropertyInquirySerializer(client_data)

            sorter = Sorter()

            # Update client preferences and get validated properties
            updated_client_data = sorter.update_client_preferences(client_data=serializer.data)
            validated_properties = sorter.get_pre_validated_property(updated_client_data=updated_client_data)

            if not validated_properties:
                return Response({'status': False, 'message': 'No matching properties found'}, status=status.HTTP_404_NOT_FOUND)

            scored_units = []
            for property in validated_properties:
                scored_properties = sorter.calculate_property_score(client_preferences=updated_client_data, unit_id=property)
                scored_units.append(scored_properties)

            sorted_data = reversed(sorted(scored_units, key=lambda x: list(x.values())[0]))


            # property_list = [
            #     {
            #         'property_id': property.id,
            #         'building_id': property.building_id,
            #         'bathroom_count': property.no_of_attached_bathrooms,
            #         'bedroom_type': property.unit_configuration,
            #     } for property in validated_properties
            # ]

            return Response({
                'status': True,
                'validated_properties': validated_properties,
                'property_count': len(validated_properties),
                'sorted_data':sorted_data,
            }, status=status.HTTP_200_OK)

        # except PropertyInquiry.DoesNotExist:
        #     return Response({'status': False, 'error': 'Property Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # except Exception as e:
        #     return Response({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
