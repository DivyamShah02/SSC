fgg = ['Central_Park_s_Garden', 'Multi_d_purpose_court', 'Visitors_parking', 'Gymnasium', 'Splash_pool', 'Outdoor_Swimming_pool', 'Indoor_Swimming_pool', 'Multi_d_purpose_hall', 'Banquet_hall', 'Mini_theatre', 'Indoor_games', 'Activity_room', 'Library_s_Reading_room', 'Daycare_center', 'Guest_Rooms', 'Co_d_working_space', 'Skating_s_Cycling_ring', 'Gazebo_Sit_outs', 'Senior_citizen_sit_d_outs', 'Walking_s_Jogging_track', 'Yoga_room', 'Steam_Sauna', 'Massage_room', 'Jacuzzi', 'Cafeteria', 'Card_room', 'Toddler_play_zone', 'Mud_play_zone', 'Drivers_lounge', 'House_keeping_lounge', 'On_site_waste_management', 'Solar_for_common_area', 'EV_charging_stations', 'Green_Building_Rated']

gg = ['Central Park / Garden','Mini Theatre','Senior Citizen Sit-Outs','Mud Play Zone','Multi-Purpose Court','Indoor Games','Walking / Jogging Track','Drivers Lounge','Visitors Parking','Activity Room','Yoga Room','House Keeping Lounge','Gymnasium','Library / Reading Room','Steam Sauna','On Site Waste Management','Splash Pool','Daycare Center','Massage Room','Solar For Common Area','Outdoor Swimming Pool','Guest Rooms','Jacuzzi','Ev Charging Stations','Indoor Swimming Pool','Co-Working Space','Cafeteria','Green Building Rated','Multi-Purpose Hall','Skating / Cycling Ring','Card Room','delete_amenty','Banquet Hall','Gazebo Sit Outs','Toddler Play Zone','delete_amenty']

fgg = []

for vv in gg:
    fgg.append(vv.replace(' ', '_').replace('_/_', '_s_').replace('-', '_d_'))

print(fgg)

for ind,i in enumerate(fgg):
    i = i.lower()
    new_i = i.replace('_d_', '-').replace('_s_',' / ').replace('_',' ').title()
    # print(f'{i}')
    st = f'''
<div class="col-md-3">
    <div class="form-check">
        <input class="form-check-input" type="checkbox" name="amenities" value="{i}" id="amenity{ind+1}">
        <label class="form-check-label" for="amenity{ind+1}">{new_i}</label>
    </div>
</div>
'''
    print(st)
#     st = f'''
# <div class="col-md-3">
#     <div class="form-check">
#         <input class="form-check-input" type="checkbox" name="amenities"
#             value="{i}" id="amenity{ind+1}">
#         <label class="form-check-label" for="amenity{ind+1}">{new_i}</label>
#     </div>
# </div>'''
#     print(st)
