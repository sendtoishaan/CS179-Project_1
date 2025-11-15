import random

def generate_clustered_dataset(num_nodes, filename, num_clusters=4):
    cluster_centers = []
    for _ in range(num_clusters):
        cx = random.randint(-150, 150)
        cy = random.randint(-150, 150)
        cluster_centers.append((cx, cy))
    
    with open(filename, 'w') as f:
        for i in range(num_nodes):
            center = random.choice(cluster_centers)
            spread = 50
            x = int(center[0] + random.gauss(0, spread))
            y = int(center[1] + random.gauss(0, spread))
            f.write(f"{x} {y}\n")
    
    print("Generating completed")

if __name__ == "__main__":
    generate_clustered_dataset(4096, "Clustered4096.txt", num_clusters=5)
