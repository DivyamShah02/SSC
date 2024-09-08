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

from .sorting_logic import Sorter


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
                'status': True,
                'session_id': session_id
            }, status=status.HTTP_200_OK)

        except PropertyInquiry.DoesNotExist:
            return Response({'status': False, 'error': 'Property Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    active_property = False
                    
                    if i == ind-1:
                        active_property = True
                    menu_properties.append({'property_name':property_name, 'active_property':active_property, 'ind':i+1})
                
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

            try:
                amenities_obj = Amenities.objects.get(building_id=building_id)
            except Amenities.DoesNotExist:
                raise NotFound(f"Amenties for building : {building_id} not found.")
            
            amenties_data = AmenitiesSerializer(amenities_obj).data

            property_unit_price = round((float(unit_data.get('size_of_unit')) * float(unit_data.get('per_sqft_rate_saleable'))) / 10000000, 2)

            prev_ind = False
            if ind-1 != 0:
                prev_ind = ind-1

            next_ind = False
            if ind+1 <= 15:
                next_ind = ind+1

            data = {
                'success': True, 
                'index':ind,
                'prev_ind':prev_ind,
                'next_ind':next_ind,
                'session_id':session_id,
                'amenties_data':amenties_data,
                'property_unit_price':property_unit_price,
                'menu_properties':menu_properties, 
                'main_property': building_data,
                'unit_data':unit_data,
                }
            
            return render(request, 'property_detail.html', data)
            return Response(data)
        

        except ParseError as e:
            return Response({'success': False, 'error': str(e)}, status=400)

        except NotFound as e:
            return Response({'success': False, 'error': str(e)}, status=404)

        except Exception as e:
            # Catch any other unforeseen errors
            print(e)
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

