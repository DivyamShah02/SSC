import time

from django.shortcuts import render, get_object_or_404, redirect
from django.db import DatabaseError, transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import PropertyInquirySerializer
from .models import PropertyInquiry
from .library.DistanceCalculator import get_address

import logging
logger = logging.getLogger('ClientDetail')

class PropertyInquiryViewSet(viewsets.ViewSet):

    @method_decorator(login_required(login_url='/login/'))
    def list(self, request):
        try:
            user = request.user
            group_names = user.groups.values_list('name', flat=True)

            if not user.is_staff:
                if str(group_names[0]) != 'Property Inquiry':
                    return redirect('error_page')

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
            logger.error(f"Error rendering inquiry form: {str(e)}")
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

            if data['copy_client_id'] != "NULL":
                data['copy_client_id'] = data['copy_client_id']
                inquiry_instance = get_object_or_404(PropertyInquiry, id=data['copy_client_id'])
                serializer = PropertyInquirySerializer(inquiry_instance, data=data)
            else:
                data['inquiry_added_by'] = f'{request.user.first_name} {request.user.last_name}'
                serializer = PropertyInquirySerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                logger.error(f"Inquiry successfully saved. Client ID: {serializer.data['id']}")
                return Response({"success": True, 
                                 "message": "Inquiry submitted successfully!", 
                                 "client_id": serializer.data['id']}, 
                                status=status.HTTP_201_CREATED)

            logger.error(f"Validation errors: {serializer.errors}")
            return Response({"success": False, 
                             "message": serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            logger.error(f"Validation Error: {str(ve)}")
            return Response({"success": False, 
                             "message": "Validation error occurred.", 
                             "details": str(ve)}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_err:
            logger.error(f"Database Error: {str(db_err)}")
            return Response({"success": False, 
                             "message": "A database error occurred.", 
                             "details": str(db_err)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
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
            multiple_values_fields = ['preferred_locations', 'unit_type', 'bedrooms', 'amenities', 'society_type']

            for multiple_values_field in multiple_values_fields:
                if type(client_data[multiple_values_field]) != list:
                    client_data[multiple_values_field] = [str(client_data[multiple_values_field])]


            school_area = str(client_data['school_area']).split('|')
            school_area_info = get_address(school_area[0], school_area[1])
            client_data['school_area_info'] = school_area_info
            
            workplace_area = str(client_data['workplace_area']).split('|')
            workplace_area_info = get_address(workplace_area[0], workplace_area[1])
            client_data['workplace_area_info'] = workplace_area_info

            pref_loc_address = []
            for pref_loc in client_data['preferred_locations']:
                pref_loc_cord = str(pref_loc).split('|')
                full_loc_address = get_address(pref_loc_cord[0], pref_loc_cord[1])
                loc_address_lst = full_loc_address.split(',')
                loc_address = full_loc_address
                for addr in loc_address_lst:
                    if '+' in addr:
                        continue
                    else:
                        loc_address = addr.strip()
                        break

                pref_loc_address.append({'lat':pref_loc_cord[0],'lng':pref_loc_cord[1],'name':loc_address})

            client_data['pref_loc_address'] = pref_loc_address    

            return Response({'success': True, 'client_data': client_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

