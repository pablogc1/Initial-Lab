# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:37:20 2024

@author: pablo
"""

import matplotlib.pyplot as plt
import numpy as np

def generate_sets(start_num, iterations, f):
    sets_dict = {}
    to_process = [(start_num, start_num + 1, f(start_num + 1))]  # Initialize with the first set
    seen = set()

    for _ in range(iterations):
        if not to_process:
            break
        s, s_plus_1, f_s_plus_1 = to_process.pop(0)
        sets_dict[s] = [s_plus_1, f_s_plus_1]

        if s_plus_1 not in seen:
            to_process.append((s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)))
            seen.add(s_plus_1)
        
        if f_s_plus_1 not in seen:
            to_process.append((f_s_plus_1, f_s_plus_1 + 1, f(f_s_plus_1 + 1)))
            seen.add(f_s_plus_1)

    return sets_dict

def mark_repeats_with_c(elements, repeated_elements):
    return [f"{el}(c)" if el in repeated_elements else str(el) for el in elements]

def process_levels_until_c(set_num_a, set_num_b, sets_dict):
    general_list = []
    marked_levels = []

    def get_element_name(el):
        return f"element {el} not available as set" if el not in sets_dict else el

    level_0_elements = [get_element_name(set_num_a), get_element_name(set_num_b)]
    general_list.append(level_0_elements)
    
    repeated_elements_0 = {el for el in level_0_elements if level_0_elements.count(el) > 1}
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_0)
    marked_levels.append(marked_level_0)

    print(f"\nLevel 0: {marked_level_0[0]}; {marked_level_0[1]}")
    
    current_a = sets_dict.get(set_num_a, [get_element_name(set_num_a)])
    current_b = sets_dict.get(set_num_b, [get_element_name(set_num_b)])

    undeveloped_elements = set()
    level = 1
    while True:
        level_elements = current_a + current_b
        general_list.append(level_elements)

        repeated_elements = set()
        for element in level_elements:
            if level_elements.count(element) > 1:
                repeated_elements.add(element)

        for element in level_elements:
            for level_elements_prev in general_list[:-1]:
                if element in level_elements_prev:
                    repeated_elements.add(element)

        marked_level_left = mark_repeats_with_c([get_element_name(el) for el in current_a], repeated_elements)
        marked_level_right = mark_repeats_with_c([get_element_name(el) for el in current_b], repeated_elements)

        for i in range(len(marked_levels)):
            left_size = len(general_list[i]) // 2
            marked_levels[i] = (
                mark_repeats_with_c(general_list[i][:left_size], repeated_elements) +
                mark_repeats_with_c(general_list[i][left_size:], repeated_elements)
            )

        marked_levels.append(marked_level_left + marked_level_right)

        print(f"\nLevel {level}: {', '.join(marked_level_left)}; {', '.join(marked_level_right)}")

        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            print(f"{i}th iteration repetitions: {', '.join(marked_levels[i][:left_size])}; {', '.join(marked_levels[i][left_size:])}")

        # Track undeveloped elements
        for el in current_a + current_b:
            if isinstance(el, str) and el.startswith("element"):
                try:
                    undeveloped_elements.add(float(el.split()[1]))
                except ValueError:
                    print(f"Skipping element: {el}")
            elif el not in sets_dict:
                undeveloped_elements.add(el)

        # Check if one side is fully canceled out for any level
        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                print(f"\nStopping at Level {level} because one side is fully canceled.")
                print(f"Total points: {total_points}")
                return total_points, undeveloped_elements

        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [get_element_name(num)]))
        for num in current_b:
            next_b.extend(sets_dict.get(num, [get_element_name(num)]))

        current_a = next_a
        current_b = next_b
        level += 1

def expand_undeveloped_elements(undeveloped_elements, sets_dict, f, iterations=5):
    for el in undeveloped_elements:
        s_plus_1 = el + 1
        f_s_plus_1 = f(el + 1)
        sets_dict[el] = [s_plus_1, f_s_plus_1]
        # Develop further if necessary
        to_process = [(s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)),
                      (f_s_plus_1, f(f_s_plus_1 + 1), f(f(f_s_plus_1 + 1)))]
        for _ in range(iterations):
            if not to_process:
                break
            s, s_plus_1, f_s_plus_1 = to_process.pop(0)
            if s not in sets_dict:
                sets_dict[s] = [s_plus_1, f_s_plus_1]
                to_process.append((s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)))
                to_process.append((f_s_plus_1, f(f_s_plus_1 + 1), f(f(f_s_plus_1 + 1))))

def select_and_compare(sets_dict, selected_set, f, iterations=5):
    print(f"\nComparing Set {selected_set} with other sets:")
    results = []
    compared_sets = []

    for set_num_b in list(sets_dict.keys()):  # Compare with all other sets
        if selected_set != set_num_b:
            print(f"\nComparing Set {selected_set} with Set {set_num_b}:")
            points, undeveloped_elements = process_levels_until_c(selected_set, set_num_b, sets_dict)
            results.append((set_num_b, points))
            compared_sets.append(set_num_b)

            if undeveloped_elements:
                print("\nExpanding undeveloped elements...")
                expand_undeveloped_elements(undeveloped_elements, sets_dict, f, iterations)
                print("\nRe-running the comparison after expanding undeveloped elements:")
                process_levels_until_c(selected_set, set_num_b, sets_dict)

    # Sort results by set number for plotting
    results.sort(key=lambda x: x[0])
    x_values = [set_num for set_num, _ in results]
    y_values = [points for _, points in results]
    
    # Plotting the results
    plt.plot(x_values, y_values, marker='o')
    plt.title(f'Set {selected_set} vs Other Sets')
    plt.xlabel('Set Number')
    plt.ylabel('Total Points')
    plt.grid(True)
    plt.show()

    return results

# Example of using a custom function
def custom_function(x):
    return np.sin(x)  # You can replace this with any function you like

# Generate sets using the custom function f(x)
sets_dict = generate_sets(start_num=1, iterations=100, f=custom_function)

# Display generated sets with (n) for elements that do not have a set named after them
print("Generated Sets:")
unavailable_elements = []
for key, value in sets_dict.items():
    annotated_value = []
    for el in value:
        if el not in sets_dict:
            annotated_value.append(f"{el}(n)")
            unavailable_elements.append(el)
        else:
            annotated_value.append(str(el))
    print(f"Set {key}: {annotated_value}")

# Print elements that do not have a set named after themselves
if unavailable_elements:
    print("\nElements without a set named after themselves:")
    print(sorted(set(unavailable_elements)))

# Function to select any set and compare with others
select_and_compare(sets_dict, selected_set=1, f=custom_function)  # Replace 5 with any set you want to compare
