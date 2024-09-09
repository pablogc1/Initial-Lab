# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 22:00:25 2024

@author: pablo
"""

import random
import matplotlib.pyplot as plt

def generate_sets(num_sets, num_elements):
    # Create a list of the first num_sets numbers (0 to num_sets-1)
    available_numbers = list(range(num_sets))

    # Initialize an empty list to store the unique sets
    list_of_sets = []

    # Generate num_sets unique sets of num_elements random numbers from the available numbers
    for i in range(num_sets):
        while True:
            random_numbers = random.sample(available_numbers, num_elements)
            # Ensure the set does not contain its own index
            if i in random_numbers:
                # Replace the element equal to the set number
                random_numbers = [num if num != i else random.choice([n for n in available_numbers if n != i]) for num in random_numbers]
            
            # Ensure the set is unique
            if random_numbers not in list_of_sets:
                list_of_sets.append(random_numbers)
                break

    return list_of_sets

def mark_repeats_with_c(elements, repeated_elements):
    """Marks repeated elements with a '(c)'."""
    return [f"{el}(c)" if el in repeated_elements else str(el) for el in elements]

def process_levels_until_c(set_num_a, set_num_b, sets_dict):
    # Initialize the general list to store all level elements for cross-level repetition checks
    general_list = []
    marked_levels = []

    # Process Level 0
    print(f"\nLevel 0: {set_num_a}; {set_num_b}")
    level_0_elements = [set_num_a, set_num_b]
    general_list.append(level_0_elements)  # Add level 0 elements to the general list
    
    # Print 0th iteration repetitions (within level 0)
    repeated_elements_0 = {el for el in level_0_elements if level_0_elements.count(el) > 1}
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_0)
    marked_levels.append(marked_level_0)
    print(f"0th iteration repetitions: {marked_level_0[0]}; {marked_level_0[1]}")

    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]

    level = 1
    while True:  # Continue indefinitely until the stopping condition is met
        print(f"\nLevel {level}: {current_a}; {current_b}")
        level_elements = current_a + current_b
        general_list.append(level_elements)  # Add the current level elements to the general list

        # Check for repetitions within the current level
        repeated_elements = set()
        for element in level_elements:
            if level_elements.count(element) > 1:
                repeated_elements.add(element)

        # Check for repetitions across all previous levels
        for element in level_elements:
            for level_elements_prev in general_list[:-1]:  # Check in all previous levels
                if element in level_elements_prev:
                    repeated_elements.add(element)

        # Mark repetitions in the current level and update previous levels
        marked_level_left = mark_repeats_with_c(current_a, repeated_elements)
        marked_level_right = mark_repeats_with_c(current_b, repeated_elements)

        # Update Level 0 and all subsequent levels with new repetitions
        for i in range(len(marked_levels)):
            left_size = len(general_list[i]) // 2
            marked_levels[i] = (
                mark_repeats_with_c(general_list[i][:left_size], repeated_elements) +
                mark_repeats_with_c(general_list[i][left_size:], repeated_elements)
            )

        marked_levels.append(marked_level_left + marked_level_right)

        # Print repetitions for the current iteration
        print(f"{level}th iteration repetitions:")
        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            print(f"{', '.join(marked_levels[i][:left_size])}; {', '.join(marked_levels[i][left_size:])}")

        # Check if one side is fully canceled out for any level
        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                print(f"\nStopping at Level {level} because one side is fully canceled.")
                # Calculate and print the total points
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                print(f"Total points: {total_points}")
                return total_points

        # Prepare for the next level
        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [num]))  # Expand sets
        for num in current_b:
            next_b.extend(sets_dict.get(num, [num]))  # Expand sets

        current_a = next_a
        current_b = next_b
        level += 1

def compare_set_1_with_others(num_sets, num_elements):
    # Generate the sets
    sets_list = generate_sets(num_sets, num_elements)
    sets_dict = {i: sets_list[i] for i in range(num_sets)}

    # Print the generated sets
    print("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        print(f"Set {idx}: {numbers_set}")

    # List to store the results
    results = []

    # Compare set 1 with all other sets
    for i in range(2, num_sets):  # Start from 2 to compare with sets 2, 3, ..., num_sets-1
        print(f"\nComparing Set 1 with Set {i}:")
        points = process_levels_until_c(1, i, sets_dict)
        results.append(points)

    # Plot the results
    plt.plot(range(2, num_sets), results, marker='o')
    plt.title('Set 1 vs Other Sets')
    plt.xlabel('Set Number')
    plt.ylabel('Total Points')
    plt.grid(True)
    plt.show()

# Example usage:
num_sets = 100  # Number of sets
num_elements = 3  # Number of elements per set

compare_set_1_with_others(num_sets, num_elements)
