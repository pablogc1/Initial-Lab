# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 17:50:10 2024

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

def process_levels(set_num_a, set_num_b):
    # Initialize the general list to store all level elements for cross-level repetition checks
    general_list = []

    # Process Level 0
    print(f"\nLevel 0: {set_num_a}; {set_num_b}")
    level_0_elements = [set_num_a, set_num_b]
    general_list.append(level_0_elements)  # Add level 0 elements to the general list
    
    # Print 0th iteration repetitions (within level 0)
    repeated_elements_0 = {el for el in level_0_elements if level_0_elements.count(el) > 1}
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_0)
    print(f"0th iteration repetitions: {marked_level_0[0]}; {marked_level_0[1]}")

    # Process Level 1
    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]
    print(f"\nLevel 1: {current_a}; {current_b}")
    level_1_elements = current_a + current_b
    general_list.append(level_1_elements)  # Add level 1 elements to the general list

    # Check for repetitions in level 1 and across level 0
    repeated_elements_1 = set()
    
    # Check within level 1
    for element in level_1_elements:
        if level_1_elements.count(element) > 1:
            repeated_elements_1.add(element)
    
    # Check across levels
    for element in level_1_elements:
        for level_elements in general_list[:-1]:  # Check in all previous levels
            if element in level_elements:
                repeated_elements_1.add(element)

    # Mark repetitions in level 1 and level 0
    marked_level_1_left = mark_repeats_with_c(current_a, repeated_elements_1)
    marked_level_1_right = mark_repeats_with_c(current_b, repeated_elements_1)
    
    # Print 1st iteration repetitions (level 0 and level 1)
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_1)
    print(f"1st iteration repetitions:")
    print(f"{marked_level_0[0]}; {marked_level_0[1]}")
    print(f"{', '.join(marked_level_1_left)}; {', '.join(marked_level_1_right)}")

    # Process Level 2
    next_a = []
    next_b = []
    for num in current_a:
        next_a.extend(sets_dict.get(num, [num]))  # Expand sets
    for num in current_b:
        next_b.extend(sets_dict.get(num, [num]))  # Expand sets

    print(f"\nLevel 2: {next_a}; {next_b}")
    level_2_elements = next_a + next_b
    general_list.append(level_2_elements)  # Add level 2 elements to the general list

    # Check for repetitions in level 2 and across previous levels
    repeated_elements_2 = set()
    
    # Check within level 2
    for element in level_2_elements:
        if level_2_elements.count(element) > 1:
            repeated_elements_2.add(element)
    
    # Check across all previous levels
    for element in level_2_elements:
        for level_elements in general_list[:-1]:  # Check in all previous levels
            if element in level_elements:
                repeated_elements_2.add(element)

    # Mark repetitions in level 2, level 1, and level 0
    marked_level_2_left = mark_repeats_with_c(next_a, repeated_elements_2)
    marked_level_2_right = mark_repeats_with_c(next_b, repeated_elements_2)
    
    # Print 2nd iteration repetitions (level 0, level 1, and level 2)
    marked_level_0 = mark_repeats_with_c(level_0_elements, repeated_elements_2)
    marked_level_1_left = mark_repeats_with_c(current_a, repeated_elements_2)
    marked_level_1_right = mark_repeats_with_c(current_b, repeated_elements_2)

    print(f"2nd iteration repetitions:")
    print(f"{marked_level_0[0]}; {marked_level_0[1]}")
    print(f"{', '.join(marked_level_1_left)}; {', '.join(marked_level_1_right)}")
    print(f"{', '.join(marked_level_2_left)}; {', '.join(marked_level_2_right)}")

# Example usage with 3 levels:
process_levels(1, 2)
