import sys
from RANDOM_SEARCH import GET_STATION_LOCATIONS
from MULTI_DRONE_SOLUTION_TRACE import GENERATE_SOLUTION_TRACE
from datetime import datetime, timedelta
from MULTI_DRONE_SOLUTION import (
    KMEANS_SINGLE_RUN,
    KMEANS_CLUSTERING,
    CLUSTER_TSP_SOLVER,
    SOLVE_MULTI_DRONE_PROBLEM,
    WRITE_ROUTE_FILES,
)


def main():
    print("ComputePossibleSolutions")
    FILE_NAME = input("Enter the name of file: ").strip()
    
    try:
        STATION_LOCATIONS = GET_STATION_LOCATIONS(FILE_NAME)
        NUM_LOCATIONS = len(STATION_LOCATIONS)

        START_TIME = datetime.now()
        COMPLETION_TIME = START_TIME + timedelta(minutes=5)
        
        try:
            COMPLETION_TIME_STRING = COMPLETION_TIME.strftime("%-I:%M%p").lower()
        except:
            COMPLETION_TIME_STRING = COMPLETION_TIME.strftime("%#I:%M%p").lower()
        
        print(f"There are {NUM_LOCATIONS} nodes: Solutions will be available by {COMPLETION_TIME_STRING}")
        

        MAX_ITERATIONS = 200
        NUM_RESTARTS = 10
        KMEANS_RESULTS = KMEANS_CLUSTERING(STATION_LOCATIONS, NUM_RESTARTS, MAX_ITERATIONS)
        
        SOLUTIONS = {}
        for K in range(1, 5):
            SOLUTION = SOLVE_MULTI_DRONE_PROBLEM(STATION_LOCATIONS, K, MAX_ITERATIONS, KMEANS_RESULTS)
            SOLUTIONS[K] = SOLUTION
        
        ROMAN_NUMERALS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        
        for K in range(1, 5):
            SOLUTION = SOLUTIONS[K]
            CLUSTER_IDS = SOLUTION['clusters']
            LANDING_PAD = SOLUTION['landing_pad']
            DISTANCES = SOLUTION['distances']
            MAX_DISTANCE = max(DISTANCES)
            
            print(f"{K}) If you use {K} drone(s), the total route will be {MAX_DISTANCE:.1f} meters")
            
            for DRONE_ID in range(K):
                CURRENT_LANDING_PAD = LANDING_PAD[DRONE_ID]
                DISTANCE = DISTANCES[DRONE_ID]
                
                NUM_LOCATIONS_IN_CLUSTER = sum(1 for cid in CLUSTER_IDS if cid == DRONE_ID)
                
                LANDING_PAD_X = int(round(CURRENT_LANDING_PAD[0]))
                LANDING_PAD_Y = int(round(CURRENT_LANDING_PAD[1]))
                
                print(f"   {ROMAN_NUMERALS[DRONE_ID]}. Landing Pad {DRONE_ID + 1} should be at [{LANDING_PAD_X},{LANDING_PAD_Y}], serving {NUM_LOCATIONS_IN_CLUSTER} locations, route is {DISTANCE:.1f} meters")
        
        while True:
            try:
                SELECTED_K = int(input("\nPlease select your choice 1 to 4: "))
                if 1 <= SELECTED_K <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        BASE_FILENAME = FILE_NAME.rsplit('.', 1)[0]
        SELECTED_SOLUTION = SOLUTIONS[SELECTED_K]
        
        WRITE_ROUTE_FILES(SELECTED_SOLUTION, BASE_FILENAME, SELECTED_K)
        GENERATE_SOLUTION_TRACE(FILE_NAME, SELECTED_SOLUTION)
        
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