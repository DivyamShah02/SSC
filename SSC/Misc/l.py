def adjust_lists(list1, list2, list3):
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

    # Adjust list1 and list3
    list1 = fill_list(list1, list2)
    list3 = fill_list(list3, list2)

    # Adjust list2 length to be a multiple of 4
    list2 = make_multiple_of_4(list2)

    # Convert lists to strings
    list1 = [str(elem) for elem in list1]
    list2 = [str(elem) for elem in list2]
    list3 = [str(elem) for elem in list3]

    return list1, list2, list3

# Example usage:
list1 = [1, 2]
list2 = [3, 4, 5]
list3 = [10, 11, 12]
new_list1, new_list2, new_list3 = adjust_lists(list1, list2, list3)

print("New List 1:", new_list1)
print("New List 2:", new_list2)
print("New List 3:", new_list3)
