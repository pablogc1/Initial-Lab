# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 21:58:50 2024

@author: pablo
"""

import matplotlib.pyplot as plt

def generate_sets(num_sets, num_elements):
    list_of_sets = []

    for i in range(num_sets):
        # Generate a set with consecutive numbers starting from the next number
        start_num = (i + 1) % num_sets  # Use modulo to wrap around the available numbers
        random_numbers = [(start_num + j) % num_sets for j in range(num_elements)]
        list_of_sets.append(random_numbers)

    return list_of_sets

def mark_repeats_with_c(elements, repeated_elements):
    return [f"{el}(c)" if el in repeated_elements else str(el) for el in elements]

def process_levels_until_c(set_num_a, set_num_b, sets_dict):
    general_list = []
    marked_levels = []

    level_0_elements = [set_num_a, set_num_b]
    general_list.append(level_0_elements)
    
    repeated_elements_0 = {el for el in level_0_elements if level_0_elements.count(el) > 1}
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_0)
    marked_levels.append(marked_level_0)

    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]

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

        marked_level_left = mark_repeats_with_c(current_a, repeated_elements)
        marked_level_right = mark_repeats_with_c(current_b, repeated_elements)

        for i in range(len(marked_levels)):
            left_size = len(general_list[i]) // 2
            marked_levels[i] = (
                mark_repeats_with_c(general_list[i][:left_size], repeated_elements) +
                mark_repeats_with_c(general_list[i][left_size:], repeated_elements)
            )

        marked_levels.append(marked_level_left + marked_level_right)

        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                return total_points

        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [num]))
        for num in current_b:
            next_b.extend(sets_dict.get(num, [num]))

        current_a = next_a
        current_b = next_b
        level += 1

def compare_all_sets(num_sets, num_elements):
    sets_list = generate_sets(num_sets, num_elements)
    sets_dict = {i: sets_list[i] for i in range(num_sets)}

    print("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        print(f"Set {idx}: {numbers_set}")

    results_matrix = []

    for i in range(num_sets):
        results_row = []
        for j in range(i, num_sets):
            points = process_levels_until_c(i, j, sets_dict)
            results_row.append(points)
        results_matrix.append(results_row)

    fig, ax = plt.subplots()
    for i, row in enumerate(results_matrix):
        ax.scatter(range(i, num_sets), row, label=f'Set {i}', s=10)

    ax.set_title('Set Comparisons')
    ax.set_xlabel('Compared Set Number')
    ax.set_ylabel('Total Points')
    ax.grid(True)
    plt.show()

# Example usage:
num_sets = 50  # Number of sets
num_elements = 2  # Number of elements per set

compare_all_sets(num_sets, num_elements)
