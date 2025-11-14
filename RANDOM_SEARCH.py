import numpy as np
import random

# Gets station locations from the given file
def GET_STATION_LOCATIONS(FILE_NAME):
    try:
        DRONE_STATION_LOCATIONS = np.loadtxt(FILE_NAME)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{FILE_NAME}' does not exist.")
    except ValueError as e:
        raise ValueError(f"Error: File '{FILE_NAME}' has invalid format.")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")
    
    if DRONE_STATION_LOCATIONS.ndim != 2:
        raise ValueError(f"Error: File must contain 2D coordinate data (rows and 2 columns).")
    
    if DRONE_STATION_LOCATIONS.shape[1] != 2:
        raise ValueError(f"Error: File must have exactly 2 columns (x, y coordinates).")
    
    LOCATIONS = len(DRONE_STATION_LOCATIONS)
    if LOCATIONS > 4096:
        raise ValueError(f"Error: Number of locations ({LOCATIONS}) exceeds the maximum limit of 256.")
    
    if LOCATIONS < 2:
        raise ValueError(f"Error: File must contain at least 2 locations. Found {LOCATIONS} location(s).")

    return DRONE_STATION_LOCATIONS

# Calculates Euclidean distance and creates a distance matrix
def CREATE_DISTANCE_MATRIX(STATION_LOCATIONS):
    NUM_OF_LOCATIONS = len(STATION_LOCATIONS) 
    DISTANCE_MATRIX = np.zeros((NUM_OF_LOCATIONS, NUM_OF_LOCATIONS))

    for i in range(NUM_OF_LOCATIONS):
        for j in range(NUM_OF_LOCATIONS):
            if i != j:
                X_POINT = (STATION_LOCATIONS[i][0] - STATION_LOCATIONS[j][0]) ** 2
                Y_POINT = (STATION_LOCATIONS[i][1] - STATION_LOCATIONS[j][1]) ** 2
                DISTANCE_MATRIX[i][j] = (X_POINT + Y_POINT) ** 0.5
    
    return DISTANCE_MATRIX

# Creates a random path starting and ending with location 1(recharge bay)
def CREATE_RANDOM_PATH(NUM_OF_STATION_LOCATIONS):
    CENTER_LOCATIONS = list(range(2, NUM_OF_STATION_LOCATIONS + 1))
    random.shuffle(CENTER_LOCATIONS)
    RANDOM_PATH = [1] + CENTER_LOCATIONS + [1]

    return RANDOM_PATH

# Calculates the total cost or overall distance of taking the specified path
def CALCULATE_PATH_DISTANCE(PATH, DISTANCE_MATRIX):
    TOTAL_DISTANCE = 0.0

    for LOCATION in range(len(PATH) - 1):
        FROM_LOCATION_X = PATH[LOCATION] - 1
        FROM_LOCATION_Y = PATH[LOCATION + 1] - 1
        TOTAL_DISTANCE += DISTANCE_MATRIX[FROM_LOCATION_X][FROM_LOCATION_Y]
    
    return TOTAL_DISTANCE

# Runs random search updating the current best solution(BSF) every time
def COMPUTE_BSF_SOLUTION(DISTANCE_MATRIX, CURRENT_PATH, CURRENT_DISTANCE):
    NUMBER_OF_LOCATIONS = len(DISTANCE_MATRIX)

    NEW_RANDOM_PATH = CREATE_RANDOM_PATH(NUMBER_OF_LOCATIONS)
    NEW_PATH_DISTANCE = CALCULATE_PATH_DISTANCE(NEW_RANDOM_PATH, DISTANCE_MATRIX)

    if NEW_PATH_DISTANCE < CURRENT_DISTANCE:
        return NEW_RANDOM_PATH, NEW_PATH_DISTANCE, True
    else:
        return CURRENT_PATH, CURRENT_DISTANCE, False



