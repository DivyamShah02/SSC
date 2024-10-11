import time

from django.shortcuts import render, get_object_or_404
from django.db import DatabaseError, transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import PropertyInquirySerializer
from .models import PropertyInquiry


class PropertyInquiryViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            return render(request, 'property_inquiry_form.html')
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

            data['number'] = data['country_code'] + " " + data['number']
            data['whatsapp'] = data['whatsapp_country_code'] + " " + data['whatsapp']

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

class UnitClientDataViewSet(viewsets.ViewSet):

    def create(self, request):
        client_id = request.data.get('client_id')
        if client_id:
            client_data_obj = get_object_or_404(PropertyInquiry, id=client_id)
            client_data = PropertyInquirySerializer(client_data_obj).data
            return Response({'success': True, 'client_data': client_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

