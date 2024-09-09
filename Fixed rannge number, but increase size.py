# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:55:37 2024

@author: pablo
"""

import random
import matplotlib.pyplot as plt

def generate_sets(num_sets, num_elements):
    available_numbers = list(range(num_sets))
    list_of_sets = []

    for i in range(num_sets):
        while True:
            random_numbers = random.sample(available_numbers, num_elements)
            if i in random_numbers:
                random_numbers = [num if num != i else random.choice([n for n in available_numbers if n != i]) for num in random_numbers]
            if random_numbers not in list_of_sets:
                list_of_sets.append(random_numbers)
                break

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

def compare_all_sets_with_multiple_additions(num_sets, num_elements, num_additions):
    sets_list = generate_sets(num_sets, num_elements)
    sets_dict = {i: sets_list[i] for i in range(num_sets)}

    print("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        print(f"Set {idx}: {numbers_set}")

    results_matrix = []
    results_matrix_with_additions = []

    # Compute the original results matrix
    for i in range(num_sets):
        results_row = []
        for j in range(i, num_sets):
            points = process_levels_until_c(i, j, sets_dict)
            results_row.append(points)
        results_matrix.append(results_row)

    # Add the additional numbers x times
    for addition in range(num_additions):
        additional_numbers = list(range(num_sets, num_sets + 100))
        for number in additional_numbers:
            random_set = random.choice(sets_list)
            random_set.append(number)
        
        sets_dict_with_extra = {i: sets_list[i] for i in range(num_sets)}

    # Compute the results matrix after all additions
    for i in range(num_sets):
        results_row = []
        for j in range(i, num_sets):
            points = process_levels_until_c(i, j, sets_dict_with_extra)
            results_row.append(points)
        results_matrix_with_additions.append(results_row)

    # Plotting only the first and last iterations
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Plot original results
    for i, row in enumerate(results_matrix):
        axs[0].scatter(range(i, num_sets), row, label=f'Set {i}', s=10)
    axs[0].set_title(f'Original Set Comparisons')
    axs[0].set_xlabel('Compared Set Number')
    axs[0].set_ylabel('Total Points')
    axs[0].grid(True)

    # Plot results after all additions
    for i, row in enumerate(results_matrix_with_additions):
        axs[1].scatter(range(i, num_sets), row, label=f'Set {i}', s=10)
    axs[1].set_title(f'Set Comparisons After {num_additions} Additions')
    axs[1].set_xlabel('Compared Set Number')
    axs[1].set_ylabel('Total Points')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

# Example usage:
num_sets = 100  # Number of sets
num_elements = 3  # Number of elements per set
num_additions = 10  # Number of times to add 100 additional elements

compare_all_sets_with_multiple_additions(num_sets, num_elements, num_additions)


