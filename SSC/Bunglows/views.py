from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import BooleanField
from django.urls import reverse
from .serializers import BunglowDetailsSerializer, BunglowAmenitiesSerializer, BunglowUnitDetailsSerializer
from .models import BunglowDetails, BunglowAmenities, BunglowUnitDetails
from django.db import transaction
import ast
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .upload_s3 import upload_to_s3_from_request_files

import logging
logger = logging.getLogger('Bunglow')

class BunglowDetailFormViewSet(viewsets.ViewSet):
    
    @method_decorator(login_required(login_url='/login/'))
    def list(self, request):
        user = request.user
        group_names = user.groups.values_list('name', flat=True)

        if not user.is_staff:
            if str(group_names[0]) != 'Building Detail':
                return redirect('error_page')

        bunglow_id = request.GET.get('bunglow_id')
        is_building_edit = False
        if bunglow_id:
            is_building_edit = True

        all_units = BunglowUnitDetails.objects.filter(bunglow_id=bunglow_id)
        has_penthouse = False
        has_duplex = False

        for unit in all_units:
            if str(unit.unit_type) == 'Duplex':
                has_duplex = True
            
            if str(unit.unit_type) == 'Penthouse':
                has_penthouse = True

        data = {
            'is_building_edit':is_building_edit,
            'bunglow_id':bunglow_id,
            'has_penthouse': has_penthouse,
            'has_duplex': has_duplex,
        }

        return render(request, 'bunglow_detail_form.html', data)

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

            # data['number'] = data['number_country_code'] + " " + data['number']
            # data['alternate_number'] = data['alternate_number_country_code'] + " " + data['alternate_number']

            try:
                last_bunglow = BunglowDetails.objects.latest('id')
                bunglow_id = int(last_bunglow.bunglow_id) + 1
            
            except BunglowDetails.DoesNotExist:
                bunglow_id = 1000

            google_pin = data['google_Pin'].split('|')
            data['google_pin_lat'], data['google_pin_lng'] = google_pin
            try:
                if type(data['amenities']) != list:
                    data['amenities'] = [data['amenities']]
                amenities_data = {amenity: True for amenity in data['amenities']}

            except Exception as ex:
                logger.error(ex, exc_info=True)
                data['amenities'] = []
                amenities_data = {amenity: True for amenity in data['amenities']}

            if data['copy_bunglow_id'] != "NULL":
                data['bunglow_id'] = data['copy_bunglow_id']
                building_instance = get_object_or_404(BunglowDetails, bunglow_id=data['copy_bunglow_id'])
                # building_serializer = BuildingDetailsSerializer(building_instance)
                building_serializer = BunglowDetailsSerializer(building_instance, data=data)

                amenities_instance = get_object_or_404(BunglowAmenities, bunglow_id=data['copy_bunglow_id'])

                for field in amenities_instance._meta.fields:
                    if isinstance(field, BooleanField):
                        setattr(amenities_instance, field.name, False)

                amenities_data['bunglow_id'] = data['copy_bunglow_id']
                amenities_obj = BunglowAmenitiesSerializer(amenities_instance, data=amenities_data)
                
                if not amenities_obj.is_valid():
                    return Response({"success": False, "errors": amenities_obj.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:    
                data['bunglow_id'] = bunglow_id
                data['bunglow_added_by'] = f'{request.user}'
                building_serializer = BunglowDetailsSerializer(data=data)
                amenities_obj = BunglowAmenities(bunglow_id=bunglow_id, **amenities_data)
            
            if not building_serializer.is_valid():
                return Response({"success": False, "errors": building_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            building_serializer.save()
            amenities_obj.save()

            all_units = BunglowUnitDetails.objects.filter(bunglow_id=building_serializer.data['bunglow_id'])
            for unit in all_units:
                unit_obj = BunglowUnitDetails.objects.get(id=unit.id)
                unit_obj.per_sqft_rate_saleable = building_serializer.data['per_sqft_rate_saleable']
                unit_obj.per_sqft_rate_saleable_penthouse = building_serializer.data['per_sqft_rate_saleable_penthouse']
                unit_obj.per_sqft_rate_saleable_duplex = building_serializer.data['per_sqft_rate_saleable_duplex']
                
                try:
                    size_of_unit = float(unit_obj.size_of_unit)                   
                    bunglow_unit_price = float(unit_obj.per_sqft_rate_saleable) * size_of_unit

                    if str(unit.unit_type) == 'Duplex':
                        bunglow_unit_price = float(unit_obj.per_sqft_rate_saleable_duplex) * size_of_unit
                    
                    if str(unit.unit_type) == 'Penthouse':
                        bunglow_unit_price = float(unit_obj.per_sqft_rate_saleable_penthouse) * size_of_unit

                    try:
                        total_development_charges = size_of_unit * float(building_serializer.data['development_charges'])
                    except:
                        total_development_charges = 0
                    
                    try:                        
                        total_advance_maintenance = size_of_unit * float(building_serializer.data['advance_maintenance'])
                    except:
                        total_advance_maintenance = 0

                    try:
                        total_maintenance_deposit = size_of_unit * float(building_serializer.data['maintenance_deposit'])
                    except:
                        total_maintenance_deposit = 0
                    
                    try:            
                        total_other_specific_expenses = size_of_unit * float(building_serializer.data['other_specific_expenses'])
                    except:
                        total_other_specific_expenses = 0

                    total_bunglow_unit_price = bunglow_unit_price + total_advance_maintenance + total_development_charges + total_maintenance_deposit + total_other_specific_expenses
                    print(bunglow_unit_price, total_advance_maintenance, total_development_charges, total_maintenance_deposit, total_other_specific_expenses)
                    unit_obj.base_price = total_bunglow_unit_price
                    bunglow_unit_price_in_cr = round((total_bunglow_unit_price) / 10000000, 2)

                except:
                    unit_obj.base_price = 0
                unit_obj.google_pin_lat = building_serializer.data['google_pin_lat']
                unit_obj.google_pin_lng = building_serializer.data['google_pin_lng']
                unit_obj.save()

            return Response({"success": True, "message": "Bunglow submitted successfully!", "building_db_id": building_serializer.data['id'], "bunglow_id":building_serializer.data['bunglow_id']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BunglowNameAutocompleteViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.GET.get('q', '')  # Get the query string from request
        if query:
            # Search for names containing the query (case-insensitive)
            building_data_obj = BunglowDetails.objects.filter(Q(group_name__icontains=query))  # Add fields as needed
            building_data = BunglowDetailsSerializer(building_data_obj, many=True)

            return Response(building_data.data)
        return Response({})


class BunglowCopyDataViewSet(viewsets.ViewSet):

    def create(self, request):
        bunglow_id = request.data.get('bunglow_id')
        if bunglow_id:
            building_data_obj = get_object_or_404(BunglowDetails, bunglow_id=bunglow_id)
            building_data = BunglowDetailsSerializer(building_data_obj).data

            for i in building_data:
                if "," in str(building_data[i]) and 'floor_rise' != i:
                    building_data[i] = [str(j).strip() for j in str(building_data[i]).split(',')]
            # TODO
            try:
                if type(building_data['type_of_apartments']) != list:
                    building_data['type_of_apartments'] = building_data['type_of_apartments'].split()
            except:
                pass
            try:
                if type(building_data['type_of_parking']) != list:
                    building_data['type_of_parking'] = building_data['type_of_parking'].split()
            except:
                pass

            building_data['amenities'] = []

            amenities_data_obj = get_object_or_404(BunglowAmenities, bunglow_id=bunglow_id)
            amenities_data = BunglowAmenitiesSerializer(amenities_data_obj).data

            for amenity in amenities_data:
                if amenities_data[amenity]:
                    building_data['amenities'].append(amenity)

            floor_rise_str = building_data['floor_rise']
            # TODO
            try:
                floor_rise = ast.literal_eval(floor_rise_str)
                building_data['floor_rise'] = floor_rise
                for floor in floor_rise:
                    building_data[f'floorPrice_{floor["floor"]}'] = floor['price']

            except:
                pass

            unit_unactive = False
            one_unit_added = False
            note = ''
            all_units = BunglowUnitDetails.objects.filter(bunglow_id=bunglow_id)

            if len(all_units) != 0:
                one_unit_added = True
                for unit in all_units:
                    if not unit.active:
                        unit_unactive = True
                        note = 'All units are not active, please Publish'
            else:
                unit_unactive = True
                note = 'You have added 0 units of this bunglow, please Add unit'

            if one_unit_added:
                unit_id = all_units[0].id
            
            else:
                unit_id = None

            building_data['unit_unactive'] = unit_unactive
            building_data['note'] = note
            building_data['one_unit_added'] = one_unit_added
            building_data['one_unit_id'] = unit_id

            return Response({'success': True, 'building_data': building_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class BunglowUnitDetailFormViewSet(viewsets.ViewSet):
    
    @method_decorator(login_required(login_url='/login/'))
    def list(self, request):
        user = request.user
        group_names = user.groups.values_list('name', flat=True)
    
        if not user.is_staff:
            if str(group_names[0]) != 'Building Detail':
                return redirect('error_page')

        bunglow_id = request.GET.get('bunglow_id')
        building_data = get_object_or_404(BunglowDetails, bunglow_id=bunglow_id)
        all_units = BunglowUnitDetails.objects.filter(bunglow_id=bunglow_id)

        return render(request, 'bunglow_unit_adder.html', {
            'all_units': all_units,
            'bunglow_id': bunglow_id,
            'building_data': building_data,
        })

    @transaction.atomic
    def create(self, request):
        # print(request.data.get('type_of_parking'))
        data = request.data.dict()
        # for key in data.keys():
        #     if isinstance(data[key], list) and key != 'amenities':
        #         print(key)
        #         print(data[key])
        #         try:                
        #             data[key] = ', '.join(data[key])
        #         except:
        #             pass


        try:
            # Handle file uploads
            try:
                extra_plans = request.FILES.getlist('uploaded_extra_plans')
                uploaded_extra_plans = upload_to_s3_from_request_files(extra_plans, f"plan/")

            except Exception as e:
                logger.error(e, exc_info=True)
                uploaded_extra_plans = []

            self.handle_file_uploads(data, request.FILES)
            try:
                building_instance = get_object_or_404(BunglowDetails, bunglow_id=data['bunglow_id'])
                building_serializer = BunglowDetailsSerializer(building_instance)

                # data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable'])
                # if str(data['unit_type']) == 'Duplex':
                #     data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable_duplex'])
                
                # if str(data['unit_type']) == 'Penthouse':
                #     data['base_price'] = float(data['size_of_unit']) * float(data['per_sqft_rate_saleable_penthouse'])



                size_of_unit = float(data['size_of_unit'])                   
                bunglow_unit_price = float(data['per_sqft_rate_saleable']) * size_of_unit

                if str(data['unit_type']) == 'Duplex':
                    bunglow_unit_price = float(data['per_sqft_rate_saleable_duplex']) * size_of_unit
                
                if str(data['unit_type']) == 'Penthouse':
                    bunglow_unit_price = float(data['per_sqft_rate_saleable_penthouse']) * size_of_unit

                try:
                    total_development_charges = size_of_unit * float(building_serializer.data['development_charges'])
                except:
                    total_development_charges = 0
                
                try:                        
                    total_advance_maintenance = size_of_unit * float(building_serializer.data['advance_maintenance'])
                except:
                    total_advance_maintenance = 0

                try:
                    total_maintenance_deposit = size_of_unit * float(building_serializer.data['maintenance_deposit'])
                except:
                    total_maintenance_deposit = 0
                
                try:            
                    total_other_specific_expenses = size_of_unit * float(building_serializer.data['other_specific_expenses'])
                except:
                    total_other_specific_expenses = 0

                total_bunglow_unit_price = bunglow_unit_price + total_advance_maintenance + total_development_charges + total_maintenance_deposit + total_other_specific_expenses
                print(bunglow_unit_price, total_advance_maintenance, total_development_charges, total_maintenance_deposit, total_other_specific_expenses)
                data['base_price'] = total_bunglow_unit_price
                bunglow_unit_price_in_cr = round((total_bunglow_unit_price) / 10000000, 2)


            except:
                data['base_price'] = 0

            if data['unit_id'] != "NULL":
                unit_instance = get_object_or_404(BunglowUnitDetails, id=data['unit_id'])
                old_extra_plans = list(unit_instance.uploaded_extra_plans)
                data['uploaded_extra_plans'] = list(unit_instance.uploaded_extra_plans) + uploaded_extra_plans
                unit_serializer = BunglowUnitDetailsSerializer(unit_instance, data=data)
        
            else:
                data['uploaded_extra_plans'] = uploaded_extra_plans
                unit_serializer = BunglowUnitDetailsSerializer(data=data)

            if unit_serializer.is_valid():
                unit_serializer.save()
                # if data['unit_id'] != "NULL":
                #     updated_unit_instance = get_object_or_404(UnitDetails, id=data['unit_id'])

                #     updated_uploaded_extra_plans = old_extra_plans + uploaded_extra_plans

                #     updated_unit_instance.uploaded_extra_plans = updated_uploaded_extra_plans
                #     updated_unit_instance.save()

                return Response({"success": True, "data": unit_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print(unit_serializer.errors)
                return Response(unit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(e, exc_info=True)
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
            unit = BunglowUnitDetails.objects.get(id=unit_id)
            unit.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except BunglowUnitDetails.DoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BunglowUnitCopyDataViewSet(viewsets.ViewSet):

    def create(self, request):
        unit_id = request.data.get('unit_id')
        if unit_id:
            unit_data_obj = get_object_or_404(BunglowUnitDetails, id=unit_id)
            unit_data = BunglowUnitDetailsSerializer(unit_data_obj).data
            return Response({'success': True, 'unit_data': unit_data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class BunglowDocumentFormViewSet(viewsets.ViewSet):

    @transaction.atomic
    def create(self, request):
        bunglow_id = request.data.get('bunglow_id')
        building_ssc_id = request.data.get('building_ssc_id')
        redirect_url_id = request.data.get('redirect_url_id')
        if not bunglow_id:
            return Response({"success": False, "message": "Building ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            building_data = BunglowDetails.objects.get(id=bunglow_id)
            self.save_documents(building_data, request.FILES)
            return redirect(f'{redirect_url_id}?bunglow_id={building_ssc_id}')
            return Response({"success": True, "message": "Documents saved successfully!"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_documents(self, building_data, files):
        """Utility to save documents for the building."""
        document_fields = ['brochure_1', 'brochure_2', 'head_image', 'sec_image_1', 'sec_image_2', 'sec_image_3', 'sec_image_4']
        for field in document_fields:
            file = files.get(field)
            if file:
                setattr(building_data, field, file)
        building_data.save()


class BunglowActiveFormViewSet(viewsets.ViewSet):

    @transaction.atomic
    def create(self, request):
        building_db_id = request.data.get('building_db_id')
        try:
            building_data = BunglowDetails.objects.get(id=building_db_id)
            building_data.active = True
            building_data.save()

            all_units = BunglowUnitDetails.objects.filter(bunglow_id=building_data.bunglow_id)
            for unit in all_units:
                unit_obj = BunglowUnitDetails.objects.get(id=unit.id)
                unit_obj.active = True
                unit_obj.save()

            return Response({"success": True, "message": "Bunglow activated", "units": all_units.count()}, status=status.HTTP_200_OK)
        except BunglowDetails.DoesNotExist:
            return Response({"success": False, "message": "Building not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
