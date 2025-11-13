# Functions taken from RANDOM_SEARCH.py
import numpy as np
import random
from RANDOM_SEARCH import (
    GET_STATION_LOCATIONS,
    CREATE_DISTANCE_MATRIX,
    CALCULATE_PATH_DISTANCE,
)

# Nearest Neighbor approach to finding the most optimal path from location 1(recharge bay)
def NEAREST_NEIGHBOR_SEARCH(DISTANCE_MATRIX):
    NUM_OF_LOCATIONS = len(DISTANCE_MATRIX)
    CURRENT_LOCATION = 0
    PATH = [1]
    VISITED = {0}
    
    while len(VISITED) < NUM_OF_LOCATIONS:
        NEAREST_DISTANCE = float('inf')
        NEAREST_LOCATION = None

        for LOCATION in range(NUM_OF_LOCATIONS):
            if LOCATION not in VISITED:
                DISTANCE = DISTANCE_MATRIX[CURRENT_LOCATION][LOCATION]
                if DISTANCE < NEAREST_DISTANCE:
                    NEAREST_DISTANCE = DISTANCE
                    NEAREST_LOCATION = LOCATION
    
        VISITED.add(NEAREST_LOCATION)
        PATH.append(NEAREST_LOCATION + 1)
        CURRENT_LOCATION = NEAREST_LOCATION

    PATH.append(1)
    
    return PATH


'''
Nearest Neighbor approach but swap random locations to see if there is a more optimal solution
    We got the concept from https://slowandsteadybrain.medium.com/traveling-salesman-problem-ce78187cf1f3, but we created the code on our own
'''
def TWO_OPT_SEARCH(PATH, DISTANCE_MATRIX, MAX_ITERATIONS):
    IMPROVED_PATH = PATH[:]
    
    for ITERATION in range(MAX_ITERATIONS):
        IMPROVED = False
        
        for i in range(1, len(IMPROVED_PATH) - 2):
            for j in range(i + 1, len(IMPROVED_PATH) - 1):
                CURRENT_EDGE_1_START = IMPROVED_PATH[i - 1] - 1
                CURRENT_EDGE_1_END = IMPROVED_PATH[i] - 1
                CURRENT_EDGE_2_START = IMPROVED_PATH[j] - 1
                CURRENT_EDGE_2_END = IMPROVED_PATH[j + 1] - 1

                NEW_EDGE_1_START = IMPROVED_PATH[i - 1] - 1
                NEW_EDGE_1_END = IMPROVED_PATH[j] - 1
                NEW_EDGE_2_START = IMPROVED_PATH[i] - 1
                NEW_EDGE_2_END = IMPROVED_PATH[j + 1] - 1

                CURRENT_DISTANCE = (DISTANCE_MATRIX[CURRENT_EDGE_1_START][CURRENT_EDGE_1_END] + DISTANCE_MATRIX[CURRENT_EDGE_2_START][CURRENT_EDGE_2_END])
                NEW_DISTANCE = (DISTANCE_MATRIX[NEW_EDGE_1_START][NEW_EDGE_1_END] + DISTANCE_MATRIX[NEW_EDGE_2_START][NEW_EDGE_2_END])
 
                if NEW_DISTANCE < CURRENT_DISTANCE:
                    IMPROVED_PATH[i:j+1] = IMPROVED_PATH[i:j+1][::-1]
                    IMPROVED = True
                    break
            
            if IMPROVED:
                break
    
        if not IMPROVED:
            break
    
    return IMPROVED_PATH

# Runs random search updating the current best solution(BSF) every time
def COMPUTE_BSF_SOLUTION(DISTANCE_MATRIX, CURRENT_PATH, CURRENT_DISTANCE):
    NUMBER_OF_LOCATIONS = len(DISTANCE_MATRIX)
    
    NEW_PATH = CURRENT_PATH[:]
    if len(NEW_PATH) > 3:
        SWAP_INDEX1 = random.randint(1, len(NEW_PATH) - 2)
        SWAP_INDEX2 = random.randint(1, len(NEW_PATH) - 2)
        NEW_PATH[SWAP_INDEX1], NEW_PATH[SWAP_INDEX2] = NEW_PATH[SWAP_INDEX2], NEW_PATH[SWAP_INDEX1]
    
    NEW_IMPROVED_PATH = TWO_OPT_SEARCH(NEW_PATH, DISTANCE_MATRIX, 100)
    NEW_PATH_DISTANCE = CALCULATE_PATH_DISTANCE(NEW_IMPROVED_PATH, DISTANCE_MATRIX)
    
    if NEW_PATH_DISTANCE < CURRENT_DISTANCE:
        return NEW_IMPROVED_PATH, NEW_PATH_DISTANCE, True
    else:
        return CURRENT_PATH, CURRENT_DISTANCE, False