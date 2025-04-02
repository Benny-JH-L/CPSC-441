
# Assignment 4: The Harry Potter Reunion
#     CPSC 441 Winter 2025 | Benny Liang | 30192142


import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

VISUALIZE_ONE_GRAPH = True  # If set to False, will generate 4 graphs with each one with a corresponding edge type
# VISUALIZE_ONE_GRAPH = False
GRAPH_INFO_LOCATION = "magical_paths.txt" 
DESTINATION_NODE = "Ottawa"
infinity = 10e6

def dijkstra(graph, start, weight_index):
    """
    Dijkstra shortest path algorithm. Finds the shortest path based on an edge value indicated by `weight_index`.
    For example, if `weight_index` is 0 and an edge is: [123, 45566, 819263, 1443] it will utilize edge[0] (123) weight value to compute the shortest path for the graph.
    `graph` must be represented as an adjacency list (dictionary).
    `start` the starting node to of the algorithm.
    
    Returns a dictionary of shorest distance to all other nodes starting from `start` node, using the indicated edge weight value based from `weight_index`.
    """
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)
    shortest_distances = {node: infinity for node in graph}
    shortest_distances[start] = 0
    previous_nodes = {node: None for node in graph}  # To track the previous node for path reconstruction

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
                shortest_distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_distances, previous_nodes

def reconstruct_path(previous_nodes, end):
    path = []
    current_node = end
    
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    
    path.reverse()  # Reverse the path to get it from start to end
    return path

def dijkstra_shortest_path(graph, start, weight_index, use_normal_version):
    if (use_normal_version):
        distances, previous_nodes = dijkstra(graph, start, weight_index)
    else:
        alphas = [0.25, 0.25, 0.25, 0.25]  # Equal importance for all four attributes
        # Run Dijkstra's algorithm to minimize the combined edge weight
        distances, previous_nodes = dijkstra_minimized_path(graph, start, alphas)
        
    path_taken = reconstruct_path(previous_nodes, DESTINATION_NODE)
    return distances, path_taken


def a_star(graph, start, goal, heuristic, weights):
    """
    A* algorithm for finding the shortest path in a graph with multiple edge weights.
    
    graph: Dictionary representing the graph (adjacency list format).
    start: The starting node.
    goal: The goal node.
    heuristic: A function that provides a heuristic estimate of the distance from a node to the goal.
    weights: A list of weights [w1, w2, w3, w4] to scale the edge weight values.
    
    Returns: The shortest path as a list of nodes and the total path cost.
    """
    
    # Priority queue to store nodes with their f(n) = g(n) + h(n) value
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), start))  # (f(n), node)
    
    # g(n) - the cost from start to the current node
    g_costs = {node: float('inf') for node in graph}
    g_costs[start] = 0
    
    # Came from - to reconstruct the path
    came_from = {}
    
    while open_list:
        # Get the node with the lowest f(n) = g(n) + h(n)
        current_f, current_node = heapq.heappop(open_list)
        
        # If we've reached the goal, reconstruct the path
        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path, g_costs[goal]
        
        # Explore neighbors
        for neighbor, weights_list in graph[current_node].items():
            # Calculate the weighted sum of the edge costs
            weighted_cost = sum(weights[i] * weights_list[i] for i in range(len(weights_list)))
            
            tentative_g_cost = g_costs[current_node] + weighted_cost
            
            # If a shorter path to the neighbor has been found
            if tentative_g_cost < g_costs[neighbor]:
                came_from[neighbor] = current_node
                g_costs[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_cost, neighbor))
    
    return None, float('inf')  # Return None if no path is found

# Example heuristic function (straight-line or any domain-specific estimate)
def example_heuristic(node, goal):
    """
    Heuristic function to estimate cost from the current node to the goal.
    Replace this with a domain-specific heuristic.
    """
    # For simplicity, use zero heuristic (equivalent to Dijkstra's)
    return 0



# stuff used to minimize all 4 criteria (4 edge weights)
def normalize_weights(weights):
    min_w = min(weights)
    max_w = max(weights)
    return [(w - min_w) / (max_w - min_w) for w in weights]

def combine_weights(normalized_weights, alphas):
    return sum(alpha * weight for alpha, weight in zip(alphas, normalized_weights))

def dijkstra_minimized_path(graph, start, alphas):
    '''
    Modified Dijkstra's algorithm to find the optimal path that minimizes all four criteria (all 4 edge weights) 
    '''
    # Priority queue for Dijkstra's algorithm (stores tuples of (cost, node))
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)
    shortest_distances = {node: infinity for node in graph}
    shortest_distances[start] = 0
    previous_nodes = {node: None for node in graph}  # To track the previous node for path reconstruction
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # skip if we've already found a better path already
        if current_distance > shortest_distances[current_node]:
            continue
        
        # Explore neighbors
        for neighbor, weights in graph[current_node].items():
            # Normalize the edge weights
            normalized_weights = normalize_weights(weights)
            
            # Combine the normalized weights into a single cost
            edge_cost = combine_weights(normalized_weights, alphas)
            
            # Calculate the tentative cost to reach this neighbor
            tentative_cost = current_distance + edge_cost
            
            # If a shorter path is found, update the cost and add the neighbor to the open list
            if tentative_cost < shortest_distances[neighbor]:
                shortest_distances[neighbor] = tentative_cost
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (tentative_cost, neighbor))
    
    # Return the shortest distances and the path reconstruction
    return shortest_distances, previous_nodes

# (makes one graph)
def make_graph_visual(graph, weight_index, graph_name):
    """
    Generate graph visual using the indicated weight in the parameter.
    0 <= `weight_index`< 4.
    """
    print("Generating one graph...")
    
    G = nx.DiGraph()    # directed graph
    for node, edges in graph.items():
        # print(f"curr node: {node}")     # debug
        
        for neighbor, weights in edges.items():
            # print(f"neighbour: {neighbor} edge weight: {weights[weight_index]}")    # debug
            
            weight = weights[weight_index]
            G.add_edge(node, neighbor, weight=weight)
        print()

    pos = nx.spring_layout(G, seed=37, scale=20, k=55)

    # draw nodes and edges
    plt.figure(figsize=(10, 6), num=graph_name)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', arrows=True)

    # draw edge labels (weights)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    # show graph
    plt.show()


# (enables multiple graph generation)
def make_graph_visual_multiple(graph, weight_index, ax):
    """
    Generate graph visual using the indicated weight in the parameter.
    0 <= `weight_index`< 4. (This version enables the ability of creating more than one window for a graph)
    """
    
    G = nx.DiGraph()  # directed graph
    for node, edges in graph.items():
        # print(f"curr node: {node}")     # debug
        
        for neighbor, weights in edges.items():
            # print(f"neighbour: {neighbor} edge weight: {weights[weight_index]}")    # debug
            
            weight = weights[weight_index]
            G.add_edge(node, neighbor, weight=weight)
        print()

    pos = nx.spring_layout(G, seed=37, scale=20, k=55)
    ax.clear()

    # draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', arrows=True, ax=ax)

    # draw edge labels (weights)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax= ax)


# function to generate all the graphs based on edge seprate values
def make_all_graphs():
    print("Generating multiple graphs...")
    
    graph_name1= "Graph with edges as No. of Hops"
    graph_name2 = "Graph with edges as Distance (km)"
    graph_name3 = "Graph with edges as Time (hrs)"
    graph_name4 = "Graph with edges as No. Dementors"
    

    fig1, ax1 = plt.subplots(figsize=(7, 5), num=graph_name1)
    make_graph_visual_multiple(graph, weight_keys[0], ax1)

    fig2, ax2 = plt.subplots(figsize=(7, 5), num=graph_name2)
    make_graph_visual_multiple(graph, weight_keys[1], ax2)
    
    fig3, ax3 = plt.subplots(figsize=(7, 5), num=graph_name3)
    make_graph_visual_multiple(graph, weight_keys[2], ax3)

    fig4, ax4 = plt.subplots(figsize=(7, 5), num=graph_name4)
    make_graph_visual_multiple(graph, weight_keys[3], ax4)
    plt.show()

def print_graph(graph):
    print("---Graph---")
    for key in graph.keys():
        print(f"{key}: {graph[key]}")
    print("------\n")

if __name__ == "__main__":
    
    # open the file containing the graph information
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
    # debug
    # print(f"{graph_uncondensed}\n")
    print("uncondensed: ")
    print_graph(graph_uncondensed)
    
    # condense the graph (ie remove dup edges by taking the min values of each),
    # for example, graph[start][destination] has values [[123, 123, 123, 4], [1, 123, 123, 123], [123, 2, 123, 123]]
    # then the condensed version will be graph[start][destination] has values [1, 2, 123, 4]
    graph = defaultdict(dict, {})
    for key in graph_uncondensed.keys():
        # print(f"initial: {key}")    # debug
        
        for destination_key in graph_uncondensed[key].keys():
            # print(f"destination: {destination_key}")    # debug
            new_edge_info = [infinity, infinity, infinity, infinity] # -> [<no. hops>, <distance (km)>, <time (hr)>, <dementor count>]
            
            for info in graph_uncondensed[key][destination_key]:
                # print(f"{info}")    # debug
                hop, distance, time, num_dementor = info
                new_edge_info = [min(new_edge_info[0], int(hop)), min(new_edge_info[1], int(distance)), min(new_edge_info[2], int(time)), min(new_edge_info[3], int(num_dementor))]
                
            graph[key][destination_key] = new_edge_info   
            # print(f"new edge info {new_edge_info}") # debug
    # debug
    # print(graph)
    print(f"condensed graph:")
    print_graph(graph)
    
    # ensure that the destination node, Ottawa, is in the graph
    if (not (DESTINATION_NODE in graph)):
        graph[DESTINATION_NODE] = {}
    
    # print(f"{graph}\n")     # debug
    print_graph(graph)          # debug
    
    alumni_locations = ["British Columbia", "Ontario", "Quebec", "Newfoundland and Labrador", "Saskatchewan",  "Nova Scotia"]
    alumni_names = ["Harry", "Hermione", "Ron", "Luna", "Neville", "Ginny"]
    num_alumni = len(alumni_locations)
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
    shortest_path_type = ["Shortest Hop Path (SHP)", "Shortest Distance Path (SDP)", "Shortest Time Path (STP)", "Fewest Dementors Path (FDP)"]

    # use `dijkstra_shortest_path()` for 3 of the alumni
    print("Using pathfinding algorithm 1 [Dijkstra]")
    for x in range(0, int(num_alumni / 2)):
        
        print(f"Alumni {alumni_names[x]} optimal paths (Starting location {alumni_locations[x]}):")
        for indx in weight_keys:
            shortest_paths, path_taken = dijkstra_shortest_path(graph, alumni_locations[x], weight_keys[indx], True)
            print(f"{shortest_path_type[indx]}: {shortest_paths[DESTINATION_NODE]}\n - path taken: {path_taken}")
            # print(f"\r\t{shortest_path_type[indx]} from {alumni_locations[x]} to all other nodes: {shortest_paths}")     # debug
        print()
    
    # debug (test)
    print("Using pathfinding algorithm [MODIFIED Dijkstra]")
    for x in range(0, int(num_alumni / 2)):
        
        print(f"Alumni {alumni_names[x]} path optimizes all edge weights (Starting location {alumni_locations[x]}):")
        shortest_paths, path_taken = dijkstra_shortest_path(graph, alumni_locations[x], weight_keys[indx], False)
        print(f"Path cost that optimizes all 4 edge weights (all 4 criteria): {shortest_paths[DESTINATION_NODE]}\n - path taken: {path_taken}\n")
        
    # debug (see if A* does it right on the above alumni)
    # hammer_weights = [1, 1, 1, 1]
    # print("Using pathfinding algorithm 2 [A*]")
    # for x in range(0, int(num_alumni / 2)):
        
    #     print(f"Alumni {alumni_names[x]} optimal paths (Starting location {alumni_locations[x]}):")
    #     path, cost = a_star(graph, alumni_locations[x], DESTINATION_NODE, example_heuristic, hammer_weights)
    #     print(f"path: {path} | cost: {cost}")
    #     # for indx in weight_keys:
    #         # print(f"{shortest_path_type[indx]}: {shortest_paths[DESTINATION_NODE]}\n - path taken: {path_taken}")
    #         # print(f"\r\t{shortest_path_type[indx]} from {alumni_locations[x]} to all other nodes: {shortest_paths}")     # debug
    #     print()
    
    
    
    # use `` for the other 3 alumni
    print("Using pathfinding algorithm 2 [NONE]")
    for x in range(int(num_alumni / 2), num_alumni):
        print(f"Alumni {alumni_names[x]} optimal paths (Starting location {alumni_locations[x]}):")

    if (VISUALIZE_ONE_GRAPH):
        graph_name = "Graph with edges as Distance (km)"
        make_graph_visual(graph, weight_keys[0], graph_name)
    else:
        # alternatively if you want to see 4 graphs each representing a edge value, ex. one for dementors, another for time, etc.
        make_all_graphs()

