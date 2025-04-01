
# Assignment 4: The Harry Potter Reunion
#     CPSC 441 Winter 2025 | Benny Liang | 30192142


import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

GRAPH_INFO_LOCATION = "magical_paths.txt" 
DESTINATION_NODE = "Ottawa"
infinity = 10e6

# def dijkstra(graph, start):
#     """
#     Dijkstra's algorithm for finding shortest paths from a start node to all other nodes.
    
#     Args:
#         graph: Dictionary representing the graph {node: {neighbor: weight}}
#         start: Starting node
    
#     Returns:
#         Dictionary of shortest distances to each node
#         Dictionary of previous nodes for path reconstruction
#     """
#     # Initialize distances with infinity and set start node distance to 0
#     distances = {node: float('infinity') for node in graph}
#     distances[start] = 0
    
#     # Priority queue (min-heap) to select node with minimum distance
#     priority_queue = [(0, start)]
    
#     # Dictionary to keep track of previous nodes for path reconstruction
#     previous_nodes = {node: None for node in graph}
    
#     while priority_queue:
#         current_distance, current_node = heapq.heappop(priority_queue)
        
#         # Skip if we've already found a better path
#         if current_distance > distances[current_node]:
#             continue
            
#         # Explore neighbors
#         for neighbor, weight in graph[current_node].items():
#             distance = current_distance + weight
            
#             # Only consider this new path if it's better
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 previous_nodes[neighbor] = current_node
#                 heapq.heappush(priority_queue, (distance, neighbor))
    
#     return distances, previous_nodes

# def shortest_path(graph, start, end):
#     """Get the shortest path from start to end using Dijkstra's algorithm"""
#     distances, previous_nodes = dijkstra(graph, start)
    
#     path = []
#     current_node = end
    
#     # Reconstruct path by following previous nodes
#     while current_node is not None:
#         path.append(current_node)
#         current_node = previous_nodes[current_node]
    
#     # Reverse to get path from start to end
#     path = path[::-1]
    
#     return path, distances[end]

import heapq

def dijkstra(graph, start, weight_index):
    """
    Dijkstra shortest path algorithm. Finds the shortest path based on an edge value indicated by `weight_index`.
    For example, if `weight_index` is 0 and an edge is: [123, 45566, 819263, 1443] it will utilize edge[0] (123) weight value to compute the shortest path for the graph.
    `graph` must be represented as an adjacency list (dictionary).
    `start` the starting node to of the algorithm.
    
    Returns an list of shorest distance to all other nodes starting from `start` node, using the indicated edge weight value based from `weight_index`.
    """
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0

    # Dictionary to keep track of previous nodes for path reconstruction
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # skip if we've already found a better path already
        if current_distance > shortest_distances[current_node]:
            continue
        
        # print(f"current ndoe: {current_node}")  # debug
        
        for neighbor, weights in graph[current_node].items():   # get all the current node's neighbours 
            # print(f"\t{neighbor}")  # debug
            
            weight = weights[weight_index]  # select the edge weight based on `weight_index`, ex. if weight_index = 0 then we compute with respect to No. hops
            distance = current_distance + weight
            
            # If found a shorter path to neighbor, update and push to priority queue
            if distance < shortest_distances[neighbor]:
                previous_nodes[neighbor] = current_node
                shortest_distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_distances, previous_nodes


def dijkstra_shortest_path(graph, start, weight_index):
    distances, previous_nodes = dijkstra(graph, start, weight_index)

    return distances    
    # path = []
    # current_node = start
    
    # # Reconstruct path by following previous nodes
    # while current_node is not None:
    #     path.append(current_node)
    #     current_node = previous_nodes[current_node]
    
    # # Reverse to get path from start to end
    # path = path[::-1]
    
    # return path, distances[start]

# (makes one graph)
def make_graph_visual(graph, weight_index, graph_name):
    """
    Generate graph visual using the indicated weight in the parameter.
    0 <= `weight_index`< 4.
    """
    
    G = nx.DiGraph()  # Use a directed graph to maintain correct edge directions
    for node, edges in graph.items():
        print(f"curr node: {node}")     # debug
        for neighbor, weights in edges.items():
            print(f"neighbour: {neighbor} edge weight: {weights[weight_index]}")    # debug
            weight = weights[weight_index]
            G.add_edge(node, neighbor, weight=weight)
        print()

    pos = nx.spring_layout(G, seed=37, scale=20, k=55)

    # draw nodes and edges
    plt.figure(figsize=(10, 6), num=graph_name)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', arrows=True)

    # Draw edge labels (weights)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    # plt.margins(0.2)  # Adjust margins
    
    # Show plot
    plt.title("Graph Visualization with Edge Weights")
    plt.show()


# (enables multiple graph generation)
def make_graph_visual_multiple(graph, weight_index, graph_name, ax):
    """
    Generate graph visual using the indicated weight in the parameter.
    0 <= `weight_index`< 4. (This version enables the ability of creating more than one window for a graph)
    """
    
    G = nx.DiGraph()  # Use a directed graph to maintain correct edge directions
    for node, edges in graph.items():
        print(f"curr node: {node}")     # debug
        for neighbor, weights in edges.items():
            print(f"neighbour: {neighbor} edge weight: {weights[weight_index]}")    # debug
            weight = weights[weight_index]
            G.add_edge(node, neighbor, weight=weight)
        print()

    pos = nx.spring_layout(G, seed=37, scale=20, k=55)
    ax.clear()

    # draw nodes and edges
    # plt.figure(figsize=(10, 6), num=graph_name)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', arrows=True, ax=ax)

    # Draw edge labels (weights)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax= ax)
    # plt.margins(0.2)  # Adjust margins
    
    # Show plot
    # plt.title("Graph Visualization with Edge Weights")
    # plt.show()

    ax.set_title(graph_name)


def make_all_graphs():
    graph_name1 = "Graph with edges as Distance (km)"
    graph_name2 = "Graph with edges as No. of Hops"

    # Create the first figure and its subplot
    fig1, ax1 = plt.subplots(figsize=(7, 5), num="Graph 1")
    make_graph_visual_multiple(graph, weight_keys[1], graph_name1, ax1)

    # Create the second figure and its subplot
    fig2, ax2 = plt.subplots(figsize=(7, 5), num="Graph 2")
    make_graph_visual_multiple(graph, weight_keys[0], graph_name2, ax2)

    plt.show()

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
    
    # ensure that the destination node, Ottawa, is in the graph
    if (not (DESTINATION_NODE in graph)):
        graph[DESTINATION_NODE] = {}
    
    print(graph)    # debug
    
    alumni_locations = ["British Columbia", "Ontario", "Quebec", "Newfoundland and Labrador", "Saskatchewan",  "Nova Scotia"]
    # harry_start = "British Columbia"
    # hermione_start = "Ontario"
    # ron_start = "Quebec"
    # luna_start = "Newfoundland and Labrador"
    # neville_start = "Saskatchewan"
    # ginny_start = "Nova Scotia"

    # 0: No. hops
    # 1: Distance
    # 2: time
    # 3: dementors    
    weight_keys = [0, 1, 2, 3]
    weight_type = ["No. of Hops", "Distance (km)", "Time (hrs)", "Dementors"]

    shortest_paths = dijkstra_shortest_path(graph, alumni_locations[0], 0)
    print(f"\nshortest_paths from {alumni_locations[0]} to all other nodes: {shortest_paths}")
    
    # Create a figure with 2 subplots (side by side)
    # fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    graph_name = "Graph with edges as Distance (km)"
    make_graph_visual(graph, weight_keys[1], graph_name)

    # alternatively if you want to see 4 graphs each representing a edge value, ex. one for dementors, another for time, etc.
    # make_all_graphs()


