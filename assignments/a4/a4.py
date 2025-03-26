
# Assignment 4: The Harry Potter Reunion
#     CPSC 441 Winter 2025 | Benny Liang | 30192142


import heapq
from collections import defaultdict

GRAPH_INFO_LOCATION = "magical_paths.txt" 
DESTINATION_NODE = "Ottawa"
infinity = 10e6

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
        magical_path_info_unprocessed = file.readlines()
    # print(magical_path_info_unprocessed)    # debug
    
    # remove new line and white spaces
    magical_path_info_unprocessed = [item.strip() for item in magical_path_info_unprocessed]
    # print(magical_path_info_unprocessed) # debug
    
    # each edge contains the info: [<starting province>, <destination province>, <no. hops>, <distance (km)>, <time (hr)>, <dementor count>]
    edges = [magical_path_info_unprocessed[i:i+6] for i in range(0, len(magical_path_info_unprocessed), 6)]
    # print(edges)    # debug
    
    # create the graph
    # note: there are multiple magic path's from <start> to <dest> with diff edge info, so i store them as a list of lists,
    # for example: graph[start][destination] will have the edge values [[edge info 1], [edge info 2], ...], where [edge info #] contains <no. hops>, <distance (km)>, <time (hr)>, <dementor count>
    graph_uncondensed = defaultdict(lambda: defaultdict(list))   # adjacency list representation
    for edge in edges:
        start, dest, _, _, _, _ = edge
        graph_uncondensed[start][dest].append(edge[2:])       # node `start` will point to node `dest` with `edge` info (removing the `start` and `dest` from `edge` list)
    # print(graph_uncondensed)    # debug
    
    # condense the graph (ie remove dup edges by taking the min values of each),
    # for example, graph[start][destination] has values [[123, 123, 123, 4], [1, 123, 123, 123], [123, 2, 123, 123]]
    # then the condensed version will be graph[start][destination] has values [1, 2, 123, 4]
    graph = defaultdict(dict, {})
    for key in graph_uncondensed.keys():
        # print(f"{key}: {graph_uncondensed[key]}")   # debug
        # loop through all edges
        new_edge_info = [infinity, infinity, infinity, infinity] # -> [<no. hops>, <distance (km)>, <time (hr)>, <dementor count>]
        for key2 in graph_uncondensed[key]: # get list of edges
            # print(f"{key2}: {graph_uncondensed[key][key2]}") # debug
            for edge in graph_uncondensed[key][key2]:   # loop through each edge
                hop, distance, time, num_dementor = edge
                # set the new edge info as the min values
                new_edge_info = [min(new_edge_info[0], int(hop)), min(new_edge_info[1], int(distance)), min(new_edge_info[2], int(time)), min(new_edge_info[3], int(num_dementor))]
            graph[key][key2] = new_edge_info
    print(graph)    # debug
    
    harry_start = "British Columbia"
    hermione_start = "Ontario"
    ron_start = "Quebec"
    luna_start = "Newfoundland and Labrador"
    neville_start = "Saskatchewan"
    ginny_start = "Nova Scotia"
    
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

