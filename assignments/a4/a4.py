
# Assignment 4: The Harry Potter Reunion
#     CPSC 441 Winter 2025 | Benny Liang | 30192142


import heapq
from collections import defaultdict

GRAPH_INFO_LOCATION = "magical_paths.txt" 

def dijkstra(graph, start):
    """
    Dijkstra's algorithm for finding shortest paths from a start node to all other nodes.
    
    Args:
        graph: Dictionary representing the graph {node: {neighbor: weight}}
        start: Starting node
    
    Returns:
        Dictionary of shortest distances to each node
        Dictionary of previous nodes for path reconstruction
    """
    # Initialize distances with infinity and set start node distance to 0
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    # Priority queue (min-heap) to select node with minimum distance
    priority_queue = [(0, start)]
    
    # Dictionary to keep track of previous nodes for path reconstruction
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip if we've already found a better path
        if current_distance > distances[current_node]:
            continue
            
        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes

def shortest_path(graph, start, end):
    """Get the shortest path from start to end using Dijkstra's algorithm"""
    distances, previous_nodes = dijkstra(graph, start)
    
    path = []
    current_node = end
    
    # Reconstruct path by following previous nodes
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    
    # Reverse to get path from start to end
    path = path[::-1]
    
    return path, distances[end]

# Example usage
if __name__ == "__main__":
    
    with open(GRAPH_INFO_LOCATION, "r") as file:
        content = file.read()
    print(content)
    
    # # Example graph (adjacency list representation)
    # graph = defaultdict(dict, {
    #     'A': {'B': 1, 'C': 4},
    #     'B': {'A': 1, 'C': 2, 'D': 5},
    #     'C': {'A': 4, 'B': 2, 'D': 1},
    #     'D': {'B': 5, 'C': 1}
    # })
    # # graph['E']['D'] = 4 # do this to add a new entry to adj list.
    
    # print(graph)
    
    # start_node = 'A'
    # end_node = 'D'
    
    # path, distance = shortest_path(graph, start_node, end_node)
    
    # print(f"Shortest path from {start_node} to {end_node}: {' -> '.join(path)}")
    # print(f"Total distance: {distance}")

