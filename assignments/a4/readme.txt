
# Assignment 4: The Harry Potter Reunion
#     CPSC 441 Winter 2025 | Benny Liang | 30192142


---Compile/Running---
Please ensure that the following libraries are installed:
"networkx"
"matplotlib"

If they are not installed run the following in the command line:
`pip install networkx matplotlib`
these are needed libraries for graph visualization.

Like any Python code, please be in the same directory as the file and run:
`python <client/server file name>.py`

To exit the program, press the `x` at the top right of the graph visual.
If you prefer to see graphs represented by all the different edge weights, ex. No. hops, No. dementors, distance, and time.
you can uncomment the line at the bottom of `a4.py` `make_all_graphs()`, and please make sure `make_graph_visual()` above it is commented.
(So you don't have to exit that graph to see the other graphs)


---Notes about graph visual---
Please note that if there are edges going form node `n1` to `n2` and from `n2` to `n1` 
the most recently added edge (last edge) to the graph will be put overtop the other edge and made visible.
For example, an edge going from British Columbia to Saskatchewan will have a distance of 1200 km
and from Saskatchewan to British Columbia will have a distance of 1800 km
but on the graph it will only display the Saskatchewan to British Columbia distance as it was added last.


