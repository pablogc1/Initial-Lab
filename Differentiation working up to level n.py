# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:12:56 2024

@author: pablo
"""

import random

# Step 1: Create a list of the first 20 numbers (0 to 19)
first_20_numbers = list(range(20))

# Step 2: Initialize an empty list to store the unique sets
list_of_sets = []

# Step 3: Generate 20 unique sets of 3 random numbers from the first 20 numbers
for i in range(20):
    while True:
        random_numbers = random.sample(first_20_numbers, 3)
        # Ensure the set does not contain its own index
        if i in random_numbers:
            # Replace the element equal to the set number
            random_numbers = [num if num != i else random.choice([n for n in first_20_numbers if n != i]) for num in random_numbers]
        
        # Ensure the set is unique
        if random_numbers not in list_of_sets:
            list_of_sets.append(random_numbers)
            break

# Print the generated sets
print("Generated Sets:")
for idx, numbers_set in enumerate(list_of_sets):
    print(f"Set {idx}: {numbers_set}")

# Dictionary to map each number to its corresponding set
sets_dict = {i: list(list_of_sets[i]) for i in range(20)}

def mark_repeats_with_c(elements, repeated_elements):
    """Marks repeated elements with a '(c)'."""
    return [f"{el}(c)" if el in repeated_elements else str(el) for el in elements]

def process_levels(set_num_a, set_num_b, max_levels):
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

    for level in range(1, max_levels + 1):
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

        # Prepare for the next level
        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [num]))  # Expand sets
        for num in current_b:
            next_b.extend(sets_dict.get(num, [num]))  # Expand sets

        current_a = next_a
        current_b = next_b

# Example usage with up to 5 levels:
max_levels = 2  # Specify how many levels to process
process_levels(1, 2, max_levels)
