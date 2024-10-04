from Property.models import BuildingDetails, UnitDetails, Amenities
from Property.serializers import UnitDetailsSerializer, BuildingDetailsSerializer, AmenitiesSerializer
from ClientDetail.models import PropertyInquiry
from ClientDetail.serializers import PropertyInquirySerializer
from .models import ShortlistedProperty
from .serializers import ShortlistedPropertySerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ParseError
from django.shortcuts import get_object_or_404, render
import json
import ast

from .sorting_logic import Sorter
from .library.DistanceCalculator import get_distance


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
                'success': True,
                'session_id': session_id
            }, status=status.HTTP_200_OK)

        except PropertyInquiry.DoesNotExist:
            return Response({'success': False, 'error': 'Property Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyViewset(viewsets.ViewSet):
    def list(self, request):
        try:
            session_id = request.GET.get('id')

            if not session_id:
                raise ParseError("Session ID is required.")

            # Fetch session data
            session_data_obj = get_object_or_404(ShortlistedProperty, id=session_id)
            session_data = ShortlistedPropertySerializer(session_data_obj).data

            # Parse properties from session data
            properties_data_str = session_data.get('properties', '')
            if not properties_data_str:
                raise ParseError("No properties found in session data.")
            
            try:
                properties_data = json.loads(properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")

            if not isinstance(properties_data, list):
                raise ParseError("Properties data must be a list.")

            all_properties = []
            for property in properties_data[0:15]:
                try:
                    unit_id = property.get('unit_id')
                    if not unit_id:
                        raise ParseError("Unit ID is missing in property data.")

                    # Fetch unit data
                    try:
                        unit_data_obj = UnitDetails.objects.get(id=unit_id)
                    except UnitDetails.DoesNotExist:
                        raise NotFound(f"Unit with id {unit_id} not found.")
                    
                    unit_data = UnitDetailsSerializer(unit_data_obj).data

                    # Fetch building data
                    building_id = unit_data.get('building_id')
                    try:
                        building_data_obj = BuildingDetails.objects.get(building_id=building_id)
                    except BuildingDetails.DoesNotExist:
                        raise NotFound(f"Building with id {building_id} not found.")
                    
                    building_data = BuildingDetailsSerializer(building_data_obj).data

                    # Create property details
                    property_details = {
                        'unit_id': unit_id,
                        'unit_details': unit_data,
                        'building_id': building_id,
                        'building_details': building_data,
                        'score': property.get('score', 0)  # Default to 0 if score is missing
                    }

                    all_properties.append(property_details)
                except Exception as e:
                    print(e)

            return Response({'success': True, 'total_properties':len(all_properties), 'all_properties': all_properties})

        except ParseError as e:
            return Response({'success': False, 'error': str(e)}, status=400)

        except NotFound as e:
            return Response({'success': False, 'error': str(e)}, status=404)

        except Exception as e:
            # Catch any other unforeseen errors
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    def create(self, request):
        try:
            data = request.data
            session_id = data.get('id')

            if not session_id:
                raise ParseError("Session ID is required.")

            # Fetch session data
            session_data_obj = get_object_or_404(ShortlistedProperty, id=session_id)
            session_data = ShortlistedPropertySerializer(session_data_obj).data

            # Parse properties from session data
            properties_data_str = session_data.get('properties', '')
            if not properties_data_str:
                raise ParseError("No properties found in session data.")
            
            try:
                properties_data = json.loads(properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")

            if not isinstance(properties_data, list):
                raise ParseError("Properties data must be a list.")

            all_properties = []
            for property in properties_data:
                unit_id = property.get('unit_id')
                if not unit_id:
                    raise ParseError("Unit ID is missing in property data.")

                # Fetch unit data
                try:
                    unit_data_obj = UnitDetails.objects.get(id=unit_id)
                except UnitDetails.DoesNotExist:
                    raise NotFound(f"Unit with id {unit_id} not found.")
                
                unit_data = UnitDetailsSerializer(unit_data_obj).data

                # Fetch building data
                building_id = unit_data.get('building_id')
                try:
                    building_data_obj = BuildingDetails.objects.get(building_id=building_id)
                except BuildingDetails.DoesNotExist:
                    raise NotFound(f"Building with id {building_id} not found.")
                
                building_data = BuildingDetailsSerializer(building_data_obj).data

                # Create property details
                property_details = {
                    'unit_id': unit_id,
                    'unit_details': unit_data,
                    'building_id': building_id,
                    'building_details': building_data,
                    'score': property.get('score', 0)  # Default to 0 if score is missing
                }

                all_properties.append(property_details)

            return Response({'success': True, 'total_properties':len(all_properties), 'all_properties': all_properties})

        except ParseError as e:
            return Response({'success': False, 'error': str(e)}, status=400)

        except NotFound as e:
            return Response({'success': False, 'error': str(e)}, status=404)

        except Exception as e:
            # Catch any other unforeseen errors
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=500)


class PropertyDetailViewset(viewsets.ViewSet):
    def list(self, request):
        try:
            session_id = request.GET.get('session_id')
            ind = request.GET.get('ind')

            if not ind:
                raise ParseError("Property Index is required.")
            
            ind = int(ind)
            if ind > 15 or ind <= 0:
                return Response({'status':False, 'message':f'Property Index cannot be more than 15 and cannot be less than 1'})

            if not session_id:
                raise ParseError("Session ID is required.")

            # Fetch session data
            try:
                session_data_obj = ShortlistedProperty.objects.get(id=session_id)
            except ShortlistedProperty.DoesNotExist:
                raise NotFound(f"Session with id {session_id} not found.")
            session_data = ShortlistedPropertySerializer(session_data_obj).data

            # Parse properties from session data
            properties_data_str = session_data.get('properties', '')
            if not properties_data_str:
                raise ParseError("No properties found in session data.")
            
            try:
                properties_data = json.loads(properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")

            if not isinstance(properties_data, list):
                raise ParseError("Properties data must be a list.")
            
            menu_properties = []
            for i, property in enumerate(properties_data[0:15]):
                try:
                    unit_id = property.get('unit_id')
                    unit_data = UnitDetails.objects.get(id=unit_id)
                    
                    building_id = unit_data.building_id
                    building_data = BuildingDetails.objects.get(building_id=building_id)
                    
                    property_name = f'{building_id} - {building_data.name}'
                    property_group_name = building_data.group_name
                    active_property = False
                    
                    if i == ind-1:
                        active_property = True
                    menu_properties.append({'property_name':property_name, 'property_group_name':property_group_name, 'active_property':active_property, 'ind':i+1})
                
                except Exception as e:
                    print(e)

            property = properties_data[ind-1]

            unit_id = property.get('unit_id')
            if not unit_id:
                raise ParseError("Unit ID is missing in property data.")

            # Fetch unit data
            try:
                unit_data_obj = UnitDetails.objects.get(id=unit_id)
            except UnitDetails.DoesNotExist:
                raise NotFound(f"Unit with id {unit_id} not found.")
            unit_data = UnitDetailsSerializer(unit_data_obj).data


            # Fetch building data
            building_id = unit_data.get('building_id')
            try:
                building_data_obj = BuildingDetails.objects.get(building_id=building_id)
            except BuildingDetails.DoesNotExist:
                raise NotFound(f"Building with id {building_id} not found.")
            building_data = BuildingDetailsSerializer(building_data_obj).data

            lat_cord = building_data.get('google_pin_lat')
            lng_cord = building_data.get('google_pin_lng')

            # Fetch amenties data
            try:
                amenities_obj = Amenities.objects.get(building_id=building_id)
            except Amenities.DoesNotExist:
                raise NotFound(f"Amenties for building : {building_id} not found.")
            amenties_data = AmenitiesSerializer(amenities_obj).data


            # Fetch client data
            client_id = session_data.get('client_id')
            try:
                client_obj = PropertyInquiry.objects.get(id=client_id)
            except PropertyInquiry.DoesNotExist:
                raise NotFound(f"Client with id : {client_id} not found.")
            client_data = PropertyInquirySerializer(client_obj).data

            client_amenities = client_data.get('amenities')

            client_prefered_amenities = []
            other_amenities = []
            for amenity in amenties_data.keys():
                if amenties_data[amenity] == True:
                    if amenity in client_amenities:
                        amenity = str(amenity).replace('_', ' ').title()
                        client_prefered_amenities.append(amenity)
                    else:
                        amenity = str(amenity).replace('_', ' ').title()
                        other_amenities.append(amenity)

            size_of_unit = float(unit_data.get('size_of_unit'))
            property_unit_price = size_of_unit * float(unit_data.get('per_sqft_rate_saleable'))

            size_of_unit_mtrs = round(size_of_unit * 10.76, 2)

            per_sqft_rate_saleable = round(float(unit_data.get('per_sqft_rate_saleable')) / 1000, 2)

            prev_ind = False
            if ind-1 != 0:
                prev_ind = ind-1

            next_ind = False
            if ind+1 <= 15:
                next_ind = ind+1

            floor_rise_str = building_data['floor_rise']

            # Convert the string to a list of dictionaries
            floor_rise = ast.literal_eval(floor_rise_str)

            advance_maintenance_rate = round((float(building_data['advance_maintenance']) / 24), 2)
            total_advance_maintenance = size_of_unit * float(advance_maintenance_rate)
            advance_maintenance = round(total_advance_maintenance / 100000, 2)

            total_development_charges = size_of_unit * float(building_data['development_charges'])
            development_charges = round(total_development_charges / 100000, 2)
            
            print(property_unit_price)
            property_unit_price = round((property_unit_price + total_advance_maintenance + total_development_charges) / 10000000, 2)


            data = {
                'success': True, 
                'index':ind,
                'prev_ind':prev_ind,
                'next_ind':next_ind,
                'session_id':session_id,
                'amenties_data':amenties_data,
                'property_unit_price':property_unit_price,
                'per_sqft_rate_saleable':per_sqft_rate_saleable,
                'size_of_unit_mtrs':size_of_unit_mtrs,
                'menu_properties':menu_properties, 
                'main_property': building_data,
                'lat_cord':lat_cord,
                'lng_cord':lng_cord,
                'unit_data':unit_data,
                'client_data':client_data,
                'client_prefered_amenities':client_prefered_amenities,
                'other_amenities':other_amenities,
                'floor_rise':floor_rise,
                'advance_maintenance_rate':advance_maintenance_rate,
                'advance_maintenance':advance_maintenance,
                'development_charges':development_charges,
                }
            
            return render(request, 'property_detail_design.html', data)
            return Response(data)
        

        except ParseError as e:
            return Response({'success': False, 'error': str(e)}, status=400)

        except NotFound as e:
            return Response({'success': False, 'error': str(e)}, status=404)

        except Exception as e:
            # Catch any other unforeseen errors
            print(e)
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=500)


class GetDistanceViewset(viewsets.ViewSet):
    def list(self, request):
        try:
            origins = str(request.GET.get('origins')).split(',')
            destinations = str(request.GET.get('destinations')).split(',')
            distance, duration = get_distance(origins[0], origins[1], destinations[0], destinations[1])
            if distance:
                data = {
                    'success': True,
                    'duration': str(duration).title()
                }
                return Response(data, status=200)
            
            else:
                data = {
                    'success': False
                }
                return Response(data, status=400)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)
