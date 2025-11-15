import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from RANDOM_SEARCH import GET_STATION_LOCATIONS


# Visual Trace of the selected solution
def SELECTED_SOLUTION_VISUAL_TRACE(SOLUTION, STATION_LOCATIONS, FILENAME):
    COLOR_CODED_DRONES = ['red', 'blue', 'green', 'yellow']
    
    K = SOLUTION['K']
    CLUSTERS = SOLUTION['clusters']
    LANDING_PADS = SOLUTION['landing_pad']
    DRONE_ROUTES = SOLUTION['routes']
    DISTANCES = SOLUTION['distances']
    
    FIGURE, AX = plt.subplots(figsize=(14, 12))
    AX.set_aspect('equal')
    AX.grid(False)
    AX.set_facecolor('white')
    
    TITLE = f"Multi-Drone Solution - {K} Drone(s) Selected"
    AX.set_title(TITLE, fontsize=18, fontweight='bold', pad=20)
    
    NUM_OF_LOCATIONS = len(STATION_LOCATIONS)
    
    for DRONE in range(K):
        ROUTE = DRONE_ROUTES[DRONE]
        DRONE_COLOR = COLOR_CODED_DRONES[DRONE % len(COLOR_CODED_DRONES)]
        
        CLUSTER_INDICES = []
        for LOCATION_INDEX in range(NUM_OF_LOCATIONS):
            if CLUSTERS[LOCATION_INDEX] == DRONE:
                CLUSTER_INDICES.append(LOCATION_INDEX)

        ROUTE_COORDINATES = []
        LANDING_PAD = LANDING_PADS[DRONE]
        
        for NODE in ROUTE:
            if NODE == 1:
                ROUTE_COORDINATES.append(LANDING_PAD)
            else:
                CLUSTER_INDEX = NODE - 2
                if CLUSTER_INDEX < len(CLUSTER_INDICES):
                    ACTUAL_INDEX = CLUSTER_INDICES[CLUSTER_INDEX]
                    ROUTE_COORDINATES.append(STATION_LOCATIONS[ACTUAL_INDEX])
                else:
                    print(f"ERROR: NODE {NODE} -> CLUSTER_INDEX {CLUSTER_INDEX}, but cluster only has {len(CLUSTER_INDICES)} stations")
        
        for i in range(len(ROUTE_COORDINATES) - 1):
            X_START, Y_START = ROUTE_COORDINATES[i]
            X_END, Y_END = ROUTE_COORDINATES[i + 1]
            
            AX.plot(
                [X_START, X_END],
                [Y_START, Y_END],
                color=DRONE_COLOR,
                linewidth=2,
                alpha=0.7,
                zorder=2
            )
    
    for LOCATION_INDEX in range(NUM_OF_LOCATIONS):
        X, Y = STATION_LOCATIONS[LOCATION_INDEX]
        CLUSTER_ID = CLUSTERS[LOCATION_INDEX]
        COLOR = COLOR_CODED_DRONES[CLUSTER_ID % len(COLOR_CODED_DRONES)]
        
        AX.plot(X, Y, 'o', color=COLOR, markersize=4, alpha=0.8, zorder=3)
    
    for DRONE_ID in range(K):
        LANDING_PAD = LANDING_PADS[DRONE_ID]
        COLOR = COLOR_CODED_DRONES[DRONE_ID % len(COLOR_CODED_DRONES)]
        
        AX.plot(
            LANDING_PAD[0], 
            LANDING_PAD[1], 
            'o', 
            color=COLOR, 
            markersize=20, 
            markeredgecolor='black', 
            markeredgewidth=2,
            zorder=5
        )
    
    LEGEND_ELEMENTS = []
    
    for DRONE_ID in range(K):
        COLOR = COLOR_CODED_DRONES[DRONE_ID % len(COLOR_CODED_DRONES)]
        NUM_LOCATIONS_IN_CLUSTER = sum(1 for CID in CLUSTERS if CID == DRONE_ID)
        DISTANCE = DISTANCES[DRONE_ID]
        
        LABEL = f"Drone {DRONE_ID + 1}: {NUM_LOCATIONS_IN_CLUSTER} stations, {DISTANCE:.1f}m"
        LEGEND_ELEMENTS.append(Line2D([0], [0], color=COLOR, linewidth=3, label=LABEL))
    
    AX.legend(
        handles=LEGEND_ELEMENTS,
        loc='center left',
        bbox_to_anchor=(1, 0.5),
        fontsize=11,
        framealpha=0.95
    )
    
    AX.set_xlabel('X Coordinate (meters)', fontsize=14)
    AX.set_ylabel('Y Coordinate (meters)', fontsize=14)
    
    ALL_X = [loc[0] for loc in STATION_LOCATIONS] + [pad[0] for pad in LANDING_PADS]
    ALL_Y = [loc[1] for loc in STATION_LOCATIONS] + [pad[1] for pad in LANDING_PADS]
    
    X_MARGIN = (max(ALL_X) - min(ALL_X)) * 0.1
    Y_MARGIN = (max(ALL_Y) - min(ALL_Y)) * 0.1
    
    AX.set_xlim(min(ALL_X) - X_MARGIN, max(ALL_X) + X_MARGIN)
    AX.set_ylim(min(ALL_Y) - Y_MARGIN, max(ALL_Y) + Y_MARGIN)
    
    OUTPUT_FILENAME = f"{FILENAME}_K{K}_SOLUTION_TRACE.png"
    plt.tight_layout()
    plt.savefig(OUTPUT_FILENAME, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nVisualization saved as {OUTPUT_FILENAME}")
    
    plt.show()
    plt.close()


# Main function to generate visualization
def GENERATE_SOLUTION_TRACE(FILE_NAME, SELECTED_SOLUTION):
    STATION_LOCATIONS = GET_STATION_LOCATIONS(FILE_NAME)
    FILENAME = FILE_NAME.rsplit('.', 1)[0]
    
    SELECTED_SOLUTION_VISUAL_TRACE(SELECTED_SOLUTION, STATION_LOCATIONS, FILENAME)