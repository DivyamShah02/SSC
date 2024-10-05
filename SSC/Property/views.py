from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json
import time
from .serializers import BuildingDetailsSerializer, AmenitiesSerializer, UnitDetailsSerializer
from .models import BuildingDetails, Amenities, UnitDetails

class PropertyDetailFormViewSet(viewsets.ViewSet):
    def list(self, request):
        return render(request, 'property_detail_form.html')

    def create(self, request):
        # time.sleep(5)
        data = request.data

        for key in data.keys():
            if type(data[key]) == list and key != 'amenities':
                print(type(data[key]))
                try:
                    data[key] = ', '.join(data[key])
                except:
                    pass
        print(data)
        data['floor_rise'] = str(data['floor_rise'])

        last_porperty = BuildingDetails.objects.latest('id')
        building_id = int(last_porperty.building_id) + 1
        data['building_id'] = building_id

        google_pin = str(data['google_Pin']).split('|')
        google_pin_lat = google_pin[0]
        google_pin_lng = google_pin[1]

        data['google_pin_lat'] = google_pin_lat
        data['google_pin_lng'] = google_pin_lng

        building_serializer = BuildingDetailsSerializer(data=data)
        if building_serializer.is_valid():
            building_serializer.save()
            # print(building_serializer.data)
            for ind,unit in enumerate(data['units']):
                data['units'][ind]['building_id'] = building_id
                data['units'][ind]['per_sqft_rate_saleable'] = data['per_sqft_rate_saleable']
                data['units'][ind]['google_pin_lat'] = google_pin_lat
                data['units'][ind]['google_pin_lng'] = google_pin_lng

            unit_serializer = UnitDetailsSerializer(data=data['units'], many=True)
            if unit_serializer.is_valid():
                unit_serializer.save()
                print(unit_serializer.data)

                amenities_list = data['amenities']
                amenities_instance = Amenities(building_id=building_id)

                # Set fields to True based on the amenities_list
                for amenity in amenities_list:
                    if hasattr(amenities_instance, amenity):
                        setattr(amenities_instance, amenity, True)
                
                amenities_instance.save()
            # print(unit_serializer.errors)


            return Response({"success":True,"message": "Property submitted successfully!", "building_db_id":building_serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            print(building_serializer.errors)
        return Response({"success":True,"message": "Inquiry submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success":False,"message":building_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DocumentFormViewSet(viewsets.ViewSet):
    def create(self, request):
        building_id = request.data.get('building_id')
        
        if not building_id:
            return Response({"success": False, "message": "Building ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the files from the request
        brochure_1 = request.FILES.get('brochure_1')
        brochure_2 = request.FILES.get('brochure_2')
        head_image = request.FILES.get('head_image')
        sec_image_1 = request.FILES.get('sec_image_1')
        sec_image_2 = request.FILES.get('sec_image_2')
        sec_image_3 = request.FILES.get('sec_image_3')
        sec_image_4 = request.FILES.get('sec_image_4')

        # Create an instance of your DocumentDetails model to save the document files
        get_building_data = BuildingDetails.objects.get(id=building_id)
        get_building_data.brochure_1 = brochure_1
        get_building_data.brochure_2 = brochure_2

        get_building_data.head_image = head_image
        get_building_data.sec_image_1 = sec_image_1
        get_building_data.sec_image_2 = sec_image_2
        get_building_data.sec_image_3 = sec_image_3
        get_building_data.sec_image_4 = sec_image_4

        try:
            get_building_data.save()
            return Response({"success": True, "message": "Documents saved successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyActiveFormViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data

        building_db_id = data['building_db_id']

        building_data = BuildingDetails.objects.get(id=building_db_id)
        building_id = building_data.building_id

        building_data.active = True
        building_data.save()
        
        all_units = UnitDetails.objects.get(building_id=building_id)
        print(all_units.building_id)

