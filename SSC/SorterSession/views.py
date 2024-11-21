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
from django.shortcuts import get_object_or_404, render, redirect
import json
import ast
from datetime import datetime

from .sorting_logic import Sorter
from .library.DistanceCalculator import get_distance, get_address
from .visit_plan import create_visit_plan


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
                edit_session.selected_properties = ''
                edit_session.visit_details = ''

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
                    
                    property_name = f'{building_id} - {building_data.project_name}'
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
            special_amenities = [building_data[f'special_amenity_{sp}'] for sp in range(1,5) if building_data[f'special_amenity_{sp}'] != '']

            for amenity in amenties_data.keys():
                if amenties_data[amenity] == True:
                    if amenity in client_amenities:
                        amenity = str(amenity).replace('_d_', '-').replace('_s_',' / ').replace('_',' ').title()
                        client_prefered_amenities.append(amenity)
                    else:
                        amenity = str(amenity).replace('_d_', '-').replace('_s_',' / ').replace('_',' ').title()
                        other_amenities.append(amenity)

            client_prefered_amenities, other_amenities, special_amenities = self.adjust_lists(client_prefered_amenities, other_amenities, special_amenities)

            size_of_unit = float(unit_data.get('size_of_unit'))

            property_unit_price = size_of_unit * float(unit_data.get('per_sqft_rate_saleable'))
            basic_price = round(property_unit_price/ 10000000, 2)


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
            
            try:
                total_development_charges = size_of_unit * float(building_data['development_charges'])
                development_charges = round(total_development_charges / 100000, 2)
            except:
                total_development_charges = 0
                development_charges = 0

            
            try:
                advance_maintenance_rate = round((float(building_data['advance_maintenance']) / 24), 2)
                # total_advance_maintenance = size_of_unit * float(advance_maintenance_rate)
                total_advance_maintenance = size_of_unit * float(building_data['advance_maintenance'])
                advance_maintenance_per_month = advance_maintenance_rate * size_of_unit
                advance_maintenance = round(total_advance_maintenance / 100000, 2)
            except:
                advance_maintenance_rate = 0
                total_advance_maintenance = 0
                advance_maintenance = 0

            
            try:
                total_maintenance_deposit = size_of_unit * float(building_data['maintenance_deposit'])
                maintenance_deposit = round(total_maintenance_deposit / 100000, 2)
            except:
                total_maintenance_deposit = 0
                maintenance_deposit = 0

            
            try:            
                total_other_specific_expenses = size_of_unit * float(building_data['other_specific_expenses'])
                other_specific_expenses = round(total_other_specific_expenses / 100000, 2)
            except:
                total_other_specific_expenses = 0
                other_specific_expenses = 0


            try:            
                total_government_charges = (property_unit_price * (float(building_data['sale_deed_value'])/100)) * 5.9 / 100
                government_charges = round(total_government_charges / 100000, 2)
            except:
                total_government_charges = 0
                government_charges = 0

            try:            
                total_gst = (property_unit_price * (float(building_data['sale_deed_value'])/100)) * float(building_data['gst_applicable']) / 100
                gst = round(total_gst / 100000, 2)
            except:
                total_gst = 0
                gst = 0

            # total_property_unit_price = property_unit_price + total_advance_maintenance + total_development_charges + total_maintenance_deposit + total_other_specific_expenses + total_government_charges + total_gst
            total_property_unit_price = property_unit_price + total_advance_maintenance + total_development_charges + total_maintenance_deposit + total_other_specific_expenses
            property_unit_price_in_cr = round((total_property_unit_price) / 10000000, 2)

            is_ready_to_move = self.is_date_in_past(date_str=str(building_data['age_of_property_by_developer']))

            overview_keys = ['year_of_establishment','location_of_project','no_of_projects_delivered','plot_area','no_of_blocks','no_of_floors','no_of_basements','no_of_parking_allotted','type_of_parking','construction_company']
            overview_details = []
            
            for key in overview_keys:
                if key in unit_data.keys():
                    overview_details.append({'key':str(key).replace('_', ' ').title(), 'value':unit_data[key]})
                
                elif key in building_data.keys():
                    overview_details.append({'key':str(key).replace('_', ' ').title(), 'value':building_data[key]})

            
            destinations = [building_data['google_pin_lat'], building_data['google_pin_lng']]

            try:
                origins_sch = str(client_data['school_area']).split('|')
                distance_sch, duration_sch = get_distance(origins_sch[0], origins_sch[1], destinations[0], destinations[1])
                sch_info = get_address(origins_sch[0], origins_sch[1])
                duration_sch = str(duration_sch).title()
            
            except:
                duration_sch = False

            try:
                origins_work = str(client_data['workplace_area']).split('|')
                distance_work, duration_work = get_distance(origins_work[0], origins_work[1], destinations[0], destinations[1])
                work_info = get_address(origins_work[0], origins_work[1])
                duration_work = str(duration_work).title()

            except:
                duration_work = False
            

            data = {
                'success': True, 
                'index':ind,
                'prev_ind':prev_ind,
                'next_ind':next_ind,
                'session_id':session_id,
                'amenties_data':amenties_data,
                'property_unit_price_in_cr':property_unit_price_in_cr,
                'total_property_unit_price':total_property_unit_price,
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
                'special_amenities':special_amenities,
                'floor_rise':floor_rise,
                'basic_price':basic_price,
                'advance_maintenance_rate':advance_maintenance_rate,
                'advance_maintenance':advance_maintenance,
                'advance_maintenance_per_month':advance_maintenance_per_month,
                'development_charges':development_charges,
                'maintenance_deposit':maintenance_deposit,
                'other_specific_expenses':other_specific_expenses,
                'government_charges':government_charges,
                'gst':gst,
                'is_ready_to_move':is_ready_to_move,
                'overview_details':overview_details,
                'duration_sch':duration_sch,
                'duration_work':duration_work,
                'sch_info':sch_info,
                'work_info':work_info,
                'origins_sch_lat':origins_sch[0],
                'origins_sch_lng':origins_sch[1],
                'origins_work_lat':origins_work[0],
                'origins_work_lng':origins_work[1],
                }
            
            return render(request, 'property_detail_design.html', data)
            return Response(data)


        except ParseError as e:
            return redirect('error_page')
            return Response({'success': False, 'error': str(e)}, status=400)

        except NotFound as e:
            return redirect('error_page')
            return Response({'success': False, 'error': str(e)}, status=404)

        except Exception as e:
            # Catch any other unforeseen errors
            print(e)
            return redirect('error_page')
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    def is_date_in_past(self, date_str):
        input_date = datetime.strptime(date_str, "%m-%Y")
        current_date = datetime.now().replace(day=1)
        return input_date < current_date

    def adjust_lists(self, list1, list2, list3):
        # Ensure list1 and list3 have exactly 4 elements
        def fill_list(target_list, filler_list):
            while len(target_list) < 4:
                if filler_list:
                    target_list.append(filler_list.pop(0))
                else:
                    break
            return target_list

        # Make sure list2 has a length that is a multiple of 4
        def make_multiple_of_4(l):
            while len(l) % 4 != 0:
                l.pop()
            return l
        
        def rearrange_list_based_on_score(score_dict, input_list):
            return sorted(input_list, key=lambda item: score_dict.get(item, float('inf')))


        # Adjust list1 and list3
        list1 = fill_list(list1, list2)
        list3 = fill_list(list3, list2)

        # Adjust list2 length to be a multiple of 4
        list1 = make_multiple_of_4(list1)
        # list2 = make_multiple_of_4(list2)
        list3 = make_multiple_of_4(list3)

        # Convert lists to strings
        list1 = [str(elem) for elem in list1]
        list2 = [str(elem) for elem in list2]
        list3 = [str(elem) for elem in list3]

        score_dict = {'Central Park / Garden' : 1, 'Multi-Purpose Court' : 2, 'Visitors Parking' : 3, 'Gymnasium' : 4, 'Splash Pool' : 5, 'Outdoor Swimming Pool' : 6, 'Indoor Swimming Pool' : 7, 'Multi-Purpose Hall' : 8, 'Banquet Hall' : 9, 'Mini Theatre' : 10, 'Indoor Games' : 11, 'Activity Room' : 12, 'Library / Reading Room' : 13, 'Daycare Center' : 14, 'Guest Rooms' : 15, 'Co-Working Space' : 16, 'Skating / Cycling Ring' : 17, 'Gazebo Sit Outs' : 18, 'Senior Citizen Sit-Outs' : 19, 'Walking / Jogging Track' : 20, 'Yoga Room' : 21, 'Steam Sauna' : 22, 'Massage Room' : 23, 'Jacuzzi' : 24, 'Cafeteria' : 25, 'Card Room' : 26, 'Toddler Play Zone' : 27, 'Mud Play Zone' : 28, 'Drivers Lounge' : 29, 'House Keeping Lounge' : 30, 'On Site Waste Management' : 31, 'Solar For Common Area' : 32, 'Ev Charging Stations' : 33, 'Green Building Rated' : 34}

        try:
            list2 = rearrange_list_based_on_score(score_dict=score_dict, input_list=list2)[0:4]
        except:
            pass

        return list1, list2, list3


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


class SelectPropertyViewSet(viewsets.ViewSet):
    def create(self, request):
        session_id = request.data.get('session_id')
        ind = request.data.get('ind')

        try:
            session_data_obj = ShortlistedProperty.objects.get(id=session_id)
        except ShortlistedProperty.DoesNotExist:
            raise NotFound(f"Session with id {session_id} not found.")
        session_data = ShortlistedPropertySerializer(session_data_obj).data

        selected_properties_data_str = session_data.get('selected_properties', '')

        if selected_properties_data_str != '':
            try:
                selected_properties = json.loads(selected_properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")
        else:
            selected_properties = []

        properties_data_str = session_data.get('properties', '')
        properties = json.loads(properties_data_str.replace("'", '"'))

        selected_property = properties[int(ind)-1]['unit_id']

        if selected_property not in selected_properties:
            selected_properties.append(selected_property)

        session_data_obj.selected_properties = f'{selected_properties}'
        session_data_obj.save()

        return Response({'success':True}, status=200)


class VisitPlanViewSet(viewsets.ViewSet):
    def list(self, request):
        session_id = request.GET.get('session_id')

        if not session_id:
            raise ParseError("Session ID is required.")

        # Fetch session data
        try:
            session_data_obj = ShortlistedProperty.objects.get(id=session_id)
        except ShortlistedProperty.DoesNotExist:
            raise NotFound(f"Session with id {session_id} not found.")
        session_data = ShortlistedPropertySerializer(session_data_obj).data

        client_id = session_data.get('client_id')
        try:
            client_obj = PropertyInquiry.objects.get(id=client_id)
        except PropertyInquiry.DoesNotExist:
            raise NotFound(f"Client with id : {client_id} not found.")
        client_data = PropertyInquirySerializer(client_obj).data

        visit_details_data_str = session_data.get('visit_details', '')
        menu_properties = []

        if visit_details_data_str != '':
            visit_details_data = json.loads(visit_details_data_str.replace("'", '"'))

            for i, visit_unit in enumerate(visit_details_data):
                unit_id = visit_unit['unit_id']

                unit_data = UnitDetails.objects.get(id=unit_id)
                
                building_id = unit_data.building_id
                building_data = BuildingDetails.objects.get(building_id=building_id)
                
                property_name = f'{building_id} - {building_data.project_name}'
                property_group_name = building_data.group_name
                active_property = False            
                menu_properties.append({'property_name':property_name, 'property_group_name':property_group_name, 'active_property':active_property, 'ind':i+1, 'Arrival_time':visit_unit['Arrival_time'], 'Arrival_date':visit_unit['Arrival_date'], 'visit_planned':True})
                print(menu_properties)

        else:
            selected_properties_data_str = session_data.get('selected_properties', '')
            if not selected_properties_data_str:
                raise ParseError("No properties found in session data.")
            
            try:
                selected_properties_data = json.loads(selected_properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")

            if not isinstance(selected_properties_data, list):
                raise ParseError("Properties data must be a list.")
            
            for i, property in enumerate(selected_properties_data):
                try:
                    unit_id = property
                    unit_data = UnitDetails.objects.get(id=unit_id)
                    
                    building_id = unit_data.building_id
                    building_data = BuildingDetails.objects.get(building_id=building_id)
                    
                    property_name = f'{building_id} - {building_data.project_name}'
                    property_group_name = building_data.group_name
                    active_property = False            
                    menu_properties.append({'property_name':property_name, 'property_group_name':property_group_name, 'active_property':active_property, 'ind':i+1, 'visit_planned':False})
                
                except Exception as e:
                    print(e)

        data = {
            'session_id' : session_id,
            'client_data' : client_data,
            'menu_properties' : menu_properties,
        }

        return render(request, 'selected_property_detail_design.html', data)

    def create(self, request):
        start_date = request.data.get('start_date')
        start_time = request.data.get('start_time')
        start_area = request.data.get('start_area')
        session_id = request.data.get('session_id')

        date_str = f'{start_date}\n{start_time}'
        start_datetime = datetime.strptime(date_str.strip(), '%Y-%m-%d\n%H:%M')

        start_point = (str(start_area).split('|')[0], str(start_area).split('|')[1])

        try:
            session_data_obj = ShortlistedProperty.objects.get(id=session_id)
        except ShortlistedProperty.DoesNotExist:
            raise NotFound(f"Session with id {session_id} not found.")
        session_data = ShortlistedPropertySerializer(session_data_obj).data

        selected_properties_data_str = session_data.get('selected_properties', '')

        if selected_properties_data_str != '':
            try:
                selected_properties = json.loads(selected_properties_data_str.replace("'", '"'))
            except json.JSONDecodeError:
                raise ParseError("Error parsing properties data.")
        else:
            selected_properties = []

        selected_properties_coords = []
        for selected_property in selected_properties:
            selected_property_obj = UnitDetails.objects.get(id=selected_property)
            selected_properties_coords.append({"id":selected_property, "coords":(selected_property_obj.google_pin_lat, selected_property_obj.google_pin_lng)})
        
        plan = create_visit_plan(start_point, selected_properties_coords, start_datetime)
        visit_details = []
        for step in plan:
            print(f"Visit property {step['property_id']} at {step['coords']}:\n"
                    f"  Arrival_time: {step['arrival_time']}\n"
                    f"  Arrival_date: {step['arrival_date']}\n"
                    f"  Departure: {step['departure_time']}\n")
            temp_plan = {
                'unit_id':step['property_id'],
                'Arrival_time' : step['arrival_time'],
                'Arrival_date' : step['arrival_date'],
            }

            visit_details.append(temp_plan)
        
        session_data_obj.visit_details = f'{visit_details}'
        session_data_obj.save()


        return Response({'success':True}, status=200)
