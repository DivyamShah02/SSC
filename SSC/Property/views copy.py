from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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

class UnitDetailFormViewSet(viewsets.ViewSet):
    def list(self, request):
        building_id = request.GET.get('building_id')
        building_data = get_object_or_404(BuildingDetails, building_id=building_id)
        all_units = UnitDetails.objects.filter(building_id=building_id)

        data = {
            'all_units':all_units,
            'building_id':building_id,
            'building_data':building_data,
        }
        return render(request, 'unit_adder.html', data)

    def create(self, request):
        try:
            data = request.data.copy()
            print(data)
            # Handling file uploads from request.FILES
            floor_plan = request.FILES.get('floor_plan')  # Get the floor plan image
            unit_plan = request.FILES.get('unit_plan')    # Get the unit plan image

            if floor_plan:
                data['floor_plan'] = floor_plan
            else:
                data.pop('floor_plan')
            if unit_plan:
                data['unit_plan'] = unit_plan
            else:
                data.pop('unit_plan')
            print('8'*4)
            print(data)
            if data['unit_id'] != "NULL":
                print(data['unit_id'])
                data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable'])
                unit_data_instance = UnitDetails.objects.get(id=data['unit_id'])
                if unit_data_instance:
                    unit_serializer = UnitDetailsSerializer(unit_data_instance, data=data)
                    if unit_serializer.is_valid():
                        unit_serializer.save()  # Save the validated data to the database
                        
                        return Response({"success":True, "data": unit_serializer.data}, status=status.HTTP_201_CREATED)
                        building_id = data['building_id']

                        url = reverse('unit-detail-form-list')
                        return redirect(f"{url}?building_id={building_id}")
                    else:
                        print(unit_serializer.errors)
                        return Response(unit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable'])
                unit_serializer = UnitDetailsSerializer(data=data)
                if unit_serializer.is_valid():
                    unit_serializer.save()  # Save the validated data to the database
                    return Response({"success":True, "data": unit_serializer.data}, status=status.HTTP_201_CREATED)
                    
                    building_id = data['building_id']
                    url = reverse('unit-detail-form-list')
                    return redirect(f"{url}?building_id={building_id}")
                else:
                    print(unit_serializer.errors)
                    return Response(unit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'success':False})

    def delete(self, request):
            unit_id = request.data.get('unit_id')  # Get the unit ID from the request data
            
            if not unit_id:
                return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                unit = UnitDetails.objects.get(id=unit_id)  # Find the unit by ID
                print(unit_id)
                unit.delete()  # Delete the unit
                return Response({'success':True}, status=status.HTTP_204_NO_CONTENT)
            except UnitDetails.DoesNotExist:
                return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnitCopyDataViewSet(viewsets.ViewSet):
    def create(self, request):
        post_data = request.data
        unit_id = post_data['unit_id']
        print(unit_id)
        if unit_id:
            unit_data_obj = get_object_or_404(UnitDetails, id=unit_id)
            unit_data = UnitDetailsSerializer(unit_data_obj).data

            return Response({'success':True, 'unit_data':unit_data}, status=status.HTTP_200_OK)
        
        return Response({'success':False}, status=status.HTTP_400_BAD_REQUEST)

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

