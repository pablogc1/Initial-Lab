# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:31:46 2024

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

    def find_cross_repeats(current_a, current_b, all_previous_elements):
        """Find elements that are repeated across the left and right sides."""
        cross_repeats = set()
        for el in current_a:
            if el in current_b:
                cross_repeats.add(el)
            for level in all_previous_elements:
                if el in level[len(level)//2:]:
                    cross_repeats.add(el)
        
        for el in current_b:
            for level in all_previous_elements:
                if el in level[:len(level)//2]:
                    cross_repeats.add(el)
        
        return cross_repeats

    level_0_elements = [set_num_a, set_num_b]
    general_list.append(level_0_elements)
    
    marked_level_0 = mark_repeats_with_c(level_0_elements, set())
    marked_levels.append(marked_level_0)

    print(f"\nLevel 0: {marked_level_0[0]}; {marked_level_0[1]}")
    
    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]

    level = 1
    while True:
        print(f"\nLevel {level}: {current_a}; {current_b}")
        level_elements = current_a + current_b
        general_list.append(level_elements)

        cross_repeats = find_cross_repeats(current_a, current_b, general_list[:-1])

        marked_level_left = mark_repeats_with_c(current_a, cross_repeats)
        marked_level_right = mark_repeats_with_c(current_b, cross_repeats)

        for i in range(len(marked_levels)):
            left_size = len(general_list[i]) // 2
            marked_levels[i] = (
                mark_repeats_with_c(general_list[i][:left_size], cross_repeats) +
                mark_repeats_with_c(general_list[i][left_size:], cross_repeats)
            )

        marked_levels.append(marked_level_left + marked_level_right)

        print(f"{level}th iteration repetitions:")
        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            print(f"{', '.join(marked_levels[i][:left_size])}; {', '.join(marked_levels[i][left_size:])}")

        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                print(f"\nStopping at Level {level} because one side is fully canceled.")
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                print(f"Total points: {total_points}")
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

def compare_set_1_with_others(num_sets, num_elements):
    sets_list = generate_sets(num_sets, num_elements)
    sets_dict = {i: sets_list[i] for i in range(num_sets)}

    print("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        print(f"Set {idx}: {numbers_set}")

    results = []

    for i in range(2, num_sets):
        print(f"\nComparing Set 1 with Set {i}:")
        points = process_levels_until_c(1, i, sets_dict)
        results.append(points)

    plt.plot(range(2, num_sets), results, marker='o')
    plt.title('Set 1 vs Other Sets')
    plt.xlabel('Set Number')
    plt.ylabel('Total Points')
    plt.grid(True)
    plt.show()

# Example usage:
num_sets = 10  # Number of sets
num_elements = 3  # Number of elements per set

compare_set_1_with_others(num_sets, num_elements)
