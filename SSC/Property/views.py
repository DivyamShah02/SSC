from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .serializers import BuildingDetailsSerializer, AmenitiesSerializer, UnitDetailsSerializer
from .models import BuildingDetails, Amenities, UnitDetails
from django.db import transaction
import ast


class PropertyDetailFormViewSet(viewsets.ViewSet):

    def list(self, request):
        building_id = request.GET.get('building_id')
        is_building_edit = False
        if building_id:
            is_building_edit = True

        data = {
            'is_building_edit':is_building_edit,
            'building_id':building_id,
        }

        return render(request, 'property_detail_form.html', data)

    def create(self, request):
        try:
            data = request.data.copy()
            # Process list fields
            for key in data.keys():
                if isinstance(data[key], list) and key != 'amenities':
                    try:                
                        data[key] = ', '.join(data[key])
                    except:
                        pass

            data['floor_rise'] = str(data.get('floor_rise', ''))

            last_property = BuildingDetails.objects.latest('id')
            building_id = int(last_property.building_id) + 1

            google_pin = data['google_Pin'].split('|')
            data['google_pin_lat'], data['google_pin_lng'] = google_pin

            amenities_data = {amenity: True for amenity in data['amenities']}

            if data['copy_building_id'] != "NULL":
                data['building_id'] = data['copy_building_id']
                building_instance = get_object_or_404(BuildingDetails, building_id=data['copy_building_id'])
                building_serializer = BuildingDetailsSerializer(building_instance, data=data)

                amenities_instance = get_object_or_404(Amenities, building_id=data['copy_building_id'])
                amenities_data['building_id'] = data['copy_building_id']
                amenities_obj = AmenitiesSerializer(amenities_instance, data=amenities_data)
                
                if not amenities_obj.is_valid():
                    return Response({"success": False, "errors": amenities_obj.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:    
                data['building_id'] = building_id
                building_serializer = BuildingDetailsSerializer(data=data)
                amenities_obj = Amenities(building_id=building_id, **amenities_data)
            
            if not building_serializer.is_valid():
                return Response({"success": False, "errors": building_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            building_serializer.save()
            amenities_obj.save()

            return Response({"success": True, "message": "Property submitted successfully!", "building_db_id": building_serializer.data['id'], "building_id":building_serializer.data['building_id']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PropertyCopyDataViewSet(viewsets.ViewSet):

    def create(self, request):
        building_id = request.data.get('building_id')
        if building_id:
            building_data_obj = get_object_or_404(BuildingDetails, building_id=building_id)
            building_data = BuildingDetailsSerializer(building_data_obj).data

            for i in building_data:
                if "," in str(building_data[i]) and 'floor_rise' != i:
                    building_data[i] = [str(j).strip() for j in str(building_data[i]).split(',')]

            if type(building_data['type_of_apartments']) != list:
                building_data['type_of_apartments'] = building_data['type_of_apartments'].split()

            building_data['amenities'] = []

            amenities_data_obj = get_object_or_404(Amenities, building_id=building_id)
            amenities_data = AmenitiesSerializer(amenities_data_obj).data

            for amenity in amenities_data:
                if amenities_data[amenity]:
                    building_data['amenities'].append(amenity)

            floor_rise_str = building_data['floor_rise']
            
            floor_rise = ast.literal_eval(floor_rise_str)
            building_data['floor_rise'] = floor_rise

            for floor in floor_rise:
                building_data[f'floorPrice_{floor["floor"]}'] = floor['price']
            
            unit_unactive = False
            note = ''
            all_units = UnitDetails.objects.filter(building_id=building_id)
            if len(all_units) != 0:
                for unit in all_units:
                    if not unit.active:
                        unit_unactive = True
                        note = 'All units are not active, please Publish'
            else:
                unit_unactive = True
                note = 'You have added 0 units of this property, please Add unit'

            building_data['unit_unactive'] = unit_unactive
            building_data['note'] = note

            return Response({'success': True, 'building_data': building_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class UnitDetailFormViewSet(viewsets.ViewSet):

    def list(self, request):
        building_id = request.GET.get('building_id')
        building_data = get_object_or_404(BuildingDetails, building_id=building_id)
        all_units = UnitDetails.objects.filter(building_id=building_id)

        return render(request, 'unit_adder.html', {
            'all_units': all_units,
            'building_id': building_id,
            'building_data': building_data,
        })

    @transaction.atomic
    def create(self, request):
        data = request.data.dict()

        try:
            # Handle file uploads
            self.handle_file_uploads(data, request.FILES)

            data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable'])

            if data['unit_id'] != "NULL":
                unit_instance = get_object_or_404(UnitDetails, id=data['unit_id'])
                unit_serializer = UnitDetailsSerializer(unit_instance, data=data)
            else:
                unit_serializer = UnitDetailsSerializer(data=data)

            if unit_serializer.is_valid():
                unit_serializer.save()
                return Response({"success": True, "data": unit_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(unit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_file_uploads(self, data, files):
        """Utility to handle file uploads and update data dict."""
        file_fields = ['floor_plan', 'unit_plan']
        for field in file_fields:
            file = files.get(field)
            if file:
                data[field] = file
            else:
                data.pop(field, None)

    def delete(self, request):
        unit_id = request.data.get('unit_id')
        if not unit_id:
            return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = UnitDetails.objects.get(id=unit_id)
            unit.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except UnitDetails.DoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnitCopyDataViewSet(viewsets.ViewSet):

    def create(self, request):
        unit_id = request.data.get('unit_id')
        if unit_id:
            unit_data_obj = get_object_or_404(UnitDetails, id=unit_id)
            unit_data = UnitDetailsSerializer(unit_data_obj).data
            return Response({'success': True, 'unit_data': unit_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class DocumentFormViewSet(viewsets.ViewSet):

    @transaction.atomic
    def create(self, request):
        building_id = request.data.get('building_id')
        if not building_id:
            return Response({"success": False, "message": "Building ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            building_data = BuildingDetails.objects.get(id=building_id)
            self.save_documents(building_data, request.FILES)
            return Response({"success": True, "message": "Documents saved successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_documents(self, building_data, files):
        """Utility to save documents for the building."""
        document_fields = ['brochure_1', 'brochure_2', 'head_image', 'sec_image_1', 'sec_image_2', 'sec_image_3', 'sec_image_4']
        for field in document_fields:
            file = files.get(field)
            if file:
                setattr(building_data, field, file)
        building_data.save()


class PropertyActiveFormViewSet(viewsets.ViewSet):

    @transaction.atomic
    def create(self, request):
        building_db_id = request.data.get('building_db_id')
        try:
            building_data = BuildingDetails.objects.get(id=building_db_id)
            building_data.active = True
            building_data.save()

            all_units = UnitDetails.objects.filter(building_id=building_data.building_id)
            for unit in all_units:
                unit_obj = UnitDetails.objects.get(id=unit.id)
                unit_obj.active = True
                unit_obj.save()

            return Response({"success": True, "message": "Property activated", "units": all_units.count()}, status=status.HTTP_200_OK)
        except BuildingDetails.DoesNotExist:
            return Response({"success": False, "message": "Building not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
