import graph
import grid
import pandas as pd
from IPython.display import display

                
if __name__ == '__main__': 
    # initialization
    csv_filename = "S_001_Daten.csv"        # in directory ./SEARCH_001/S001                                                                                               
    landscape = grid.Grid(csv_filename)     # Creates grid from extracted data
    g = graph.Graph(grid=landscape)         # Creates Graph with nodes
    
    # show grid
    display(landscape.df_grid)
    
    # start a* algorithm and show best path solution
    g.a_start_algorithm()
    # print(g.best_path_solution)

    # visualize the path in jupyter notebook with following code:
    # g.a_start_algorithm()
    # g.show_best_path_solution_of_a_star()