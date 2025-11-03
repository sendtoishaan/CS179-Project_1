import sys
import numpy
import threading
from RANDOM_SEARCH import (
    GET_STATION_LOCATIONS,
    CREATE_DISTANCE_MATRIX,
    CREATE_RANDOM_PATH,
    CALCULATE_PATH_DISTANCE,
)
from NEAREST_NEIGHBOR_SEARCH import(
    NEAREST_NEIGHBOR_SEARCH,
    TWO_OPT_SEARCH,
    COMPUTE_BSF_SOLUTION,
)


# Global flag to signal when user hits ENTER
STOP_FLAG = False

# Waits for User to press ENTER
def wait_for_enter():
    global STOP_FLAG
    input()
    STOP_FLAG = True

# Main function
def main():
    global STOP_FLAG
    
    print("=" * 60)
    print("DRONE DELIVERY ROUTE OPTIMIZER")
    print("=" * 60)
    print()
    
    FILE_NAME = input("Enter the name of the file: ").strip()
    
    try:
        GET_LOCATIONS = GET_STATION_LOCATIONS(FILE_NAME)
        NUMBER_OF_LOCATIONS = len(GET_LOCATIONS)
        print(f"\nThere are {NUMBER_OF_LOCATIONS} nodes, computing route...")
        
        DISTANCE_MATRIX = CREATE_DISTANCE_MATRIX(GET_LOCATIONS)
        
        INITIAL_PATH = NEAREST_NEIGHBOR_SEARCH(DISTANCE_MATRIX)
        INITIAL_DISTANCE = CALCULATE_PATH_DISTANCE(INITIAL_PATH, DISTANCE_MATRIX)

        BSF_PATH = INITIAL_PATH
        BSF_DISTANCE = INITIAL_DISTANCE

        print("\nShortest Route Discovered So Far:")
        
        STOP_FLAG = False
        USER_ENTER = threading.Thread(target=wait_for_enter, daemon=True)
        USER_ENTER.start()
        
        while not STOP_FLAG:
            NEW_PATH, NEW_DISTANCE, IMPROVED = COMPUTE_BSF_SOLUTION(DISTANCE_MATRIX, BSF_PATH, BSF_DISTANCE)
            
            if IMPROVED:
                BSF_PATH = NEW_PATH
                BSF_DISTANCE = NEW_DISTANCE
                print(f"      {BSF_DISTANCE:.1f}")
        
        if BSF_DISTANCE > 6000:
            print(f"\nWARNING: Solution is {BSF_DISTANCE:.1f} meters, greater than the 6000-meter constraint.\n")

        OUTPUT_FILENAME = FILE_NAME.rsplit('.', 1)[0] + "_solution_" + str(int(BSF_DISTANCE)) + ".txt"
        
        with open(OUTPUT_FILENAME, 'w') as FHANDLE:
            FHANDLE.write(' '.join(map(str, BSF_PATH)))
        
        print(f"Route written to disk as {OUTPUT_FILENAME}")
        
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("Program aborted.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n{e}")
        print("Program aborted.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Program aborted.")
        sys.exit(1)



if __name__ == "__main__":
    main()