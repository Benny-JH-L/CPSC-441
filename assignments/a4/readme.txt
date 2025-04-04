
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

If you prefer to see different graphs represented by all the different edge weights, ex. No. hops, No. dementors, distance, and time.
you can set `VISUALIZE_ONE_GRAPH` to False at the top of `a4.py`.


---Parsing Graph Information---
Graph information is parsed from the file named `GRAPH_INFO_LOCATION` (variable set in `a4.py`) 
in the same directory as `a4.py` every 6 lines represent an edge:
line 1: Starting node
line 2: Destination node
line 3: No. Hops
line 4: Distance (km)
line 5: Time (hrs)
line 6: Dementors 


---Notes about graph visual---
Please note that if there are edges going form node `n1` to `n2` and from `n2` to `n1` 
the most recently added edge (last edge) to the graph will be put overtop the other edge and made visible.
For example, an edge going from British Columbia to Saskatchewan will have a distance of 1200 km
and from Saskatchewan to British Columbia will have a distance of 1800 km
but on the graph it will only display the Saskatchewan to British Columbia distance as it was added last.

The graph images were saved from the program output, by clicking the floppy disk at the bottom left.
