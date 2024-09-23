from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json
import time
from .serializers import BuildingDetailsSerializer, AmenitiesSerializer, UnitDetailsSerializer

class PropertyDetailFormViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'property_detail_form.html')

    def create(self, request):
        # time.sleep(5)
        data = request.data

        for key in data.keys():
            if type(data[key]) == list:
                print(type(data[key]))
                try:
                    data[key] = ', '.join(data[key])
                except:
                    pass
        print(data)
        # serializer = BuildingDetailsSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     print(serializer.data)
            # return Response({"success":True,"message": "Inquiry submitted successfully!", "client_id":serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({"success":True,"message": "Inquiry submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success":False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


