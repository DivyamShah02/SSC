import time

from django.shortcuts import render, get_object_or_404
from django.db import DatabaseError, transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import PropertyInquirySerializer
from .models import PropertyInquiry
from .library.DistanceCalculator import get_address


class PropertyInquiryViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            client_id = request.GET.get('client_id')
            is_client_edit = False
            if client_id:
                is_client_edit = True
            data = {
                'is_client_edit':is_client_edit,
                'client_id':client_id
            }

            return render(request, 'property_inquiry_form.html', data)
        except Exception as e:
            print(f"Error rendering inquiry form: {str(e)}")
            return Response({"success": False, "message": "An error occurred while loading the form."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        # transaction.on_commit(lambda: time.sleep(5))
        try:
            data = request.data

            for key in data.keys():
                if isinstance(data[key], list):
                    data[key] = ', '.join(data[key])

            # data['number'] = data['country_code'] + " " + data['number']
            # data['whatsapp'] = data['whatsapp_country_code'] + " " + data['whatsapp']

            serializer = PropertyInquirySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(f"Inquiry successfully saved. Client ID: {serializer.data['id']}")
                return Response({"success": True, 
                                 "message": "Inquiry submitted successfully!", 
                                 "client_id": serializer.data['id']}, 
                                status=status.HTTP_201_CREATED)

            print(f"Validation errors: {serializer.errors}")
            return Response({"success": False, 
                             "message": serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            print(f"Validation Error: {str(ve)}")
            return Response({"success": False, 
                             "message": "Validation error occurred.", 
                             "details": str(ve)}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_err:
            print(f"Database Error: {str(db_err)}")
            return Response({"success": False, 
                             "message": "A database error occurred.", 
                             "details": str(db_err)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({"success": False, 
                             "message": "An unexpected error occurred.", 
                             "details": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EditClientDataViewSet(viewsets.ViewSet):

    def create(self, request):
        client_id = request.data.get('client_id')
        if client_id:
            client_data_obj = get_object_or_404(PropertyInquiry, id=client_id)
            client_data = PropertyInquirySerializer(client_data_obj).data
            for i in client_data:
                if "," in str(client_data[i]):
                    client_data[i] = [str(j).strip() for j in str(client_data[i]).split(',')]

            if type(client_data['preferred_locations']) != list:
                client_data['preferred_locations'] = str(client_data['preferred_locations']).split()

            if type(client_data['unit_type']) != list:
                client_data['unit_type'] = str(client_data['unit_type']).split()

            if type(client_data['bedrooms']) != list:
                client_data['bedrooms'] = str(client_data['bedrooms']).split()

            if type(client_data['amenities']) != list:
                client_data['amenities'] = str(client_data['amenities']).split()


            school_area = str(client_data['school_area']).split('|')
            school_area_info = get_address(school_area[0], school_area[1])
            client_data['school_area_info'] = school_area_info
            
            workplace_area = str(client_data['workplace_area']).split('|')
            workplace_area_info = get_address(workplace_area[0], workplace_area[1])
            client_data['workplace_area_info'] = workplace_area_info

            print(client_data['preferred_locations'])
            pref_loc_cords = []
            for pref_loc in client_data['preferred_locations']:
                pref_loc_cord = str(pref_loc).split('|')
                pref_loc_cords.append(get_address(pref_loc_cord[0], pref_loc_cord[1]))
            
            print(pref_loc_cords)
                

            return Response({'success': True, 'client_data': client_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

