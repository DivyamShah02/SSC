g2 = ['Central Park / Garden', 'Multi-Purpose Court', 'Visitors Parking', 'Gymnasium', 'Splash Pool', 'Outdoor Swimming Pool', 'Indoor Swimming Pool', 'Multi-Purpose Hall', 'Banquet Hall', 'Mini Theatre', 'Indoor Games', 'Activity Room', 'Library / Reading Room', 'Daycare Center', 'Guest Rooms', 'Co-Working Space', 'Skating / Cycling Ring', 'Gazebo Sit Outs', 'Senior Citizen Sit-Outs', 'Walking / Jogging Track', 'Yoga Room', 'Steam Sauna', 'Massage Room', 'Jacuzzi', 'Cafeteria', 'Card Room', 'Toddler Play Zone', 'Mud Play Zone', 'Drivers Lounge', 'House Keeping Lounge', 'On Site Waste Management', 'Solar For Common Area', 'Ev Charging Stations', 'Green Building Rated', 'delete_amenty', 'delete_amenty']
print(len(g2))

# 1 2 3 4
# 5 6 7 8
# 9 10 11 12

# 1 5 9 13
# 2 6 10 14
# 3 7 11 
# 4 8 12

# 1 6 11 16
# 2 7 12 17
# 3 8 13 18
# 4 9 14 
# 5 10 15

def print_in_columns(g, columns):
    # Calculate number of rows needed
    rows = (len(g) + columns - 1) // columns  # This gives the ceiling value for rows
    res = []
    for i in range(rows):
        for j in range(i, len(g), rows):
            print(g[j], end=" ")
            # print(g[j])
            res.append(g[j])
        print()  # To move to the next line after each row
    
    return res

# Example usage
g1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
# g2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
g3 = [1,2,3,4,5,6,7,8,9,10,11,12]

# print("List 1:")
# g1_res = print_in_columns(g1, 4)  # 4 columns

print("\nList 2:")
g2_res = print_in_columns(g2, 4)  # 4 columns

# print("\nList 3:")
# g3_res = print_in_columns(g3, 4)  # 4 columns

import pdb; pdb.set_trace()

