import node 
import grid
import csv
import os
import pandas as pd

class Graph():
    
    def __init__(self, grid: grid.Grid):
        """__init__
        Initializes Graph.
        Params:
            * grid (Grid): grid object that has been constructed by the extracted data
        """
        self.grid = grid
        self.start_node = None
        self.end_node = None
        self.nodes = []
        self.adjac_list = {}
        self.best_path_solution = []
        
        self.set_nodes()
        self.set_start_end_nodes()
        self.set_adjac_list()


    def set_start_end_nodes(self):
        """set_start_end_nodes
        Initializes the start and end node for the path finding.
        """
        self.start_node = self.get_node_by_pos(self.grid.start_pos)
        self.end_node = self.get_node_by_pos(self.grid.end_pos)
    

    def set_nodes(self):
        """set_nodes
        Instantiates and initializes for every position in the grid a node object and adds it to the
        nodes-list of the graph. Also assigns all neighbour nodes to each node
        """
        for x_row in self.grid.pos_grid:
            for pos_el in x_row:
                code = self.grid.get_code_of_pos(pos_el)
                cost = self.grid.get_cost_of_pos(pos_el)
                name = self.grid.get_name_of_pos(pos_el)
                n = node.Node(cost=cost, code=code, name=name, pos=pos_el)
                self.nodes.append(n)
        self.assign_neighbour_nodes_to_nodes()
    

    def assign_neighbour_nodes_to_nodes(self):
        """assign_neighbour_nodes_to_nodes
        Assigns the neighbour nodes to each node.
        For that it iterates through all available nodes.
        It gets the position of the neighbour nodes of each node
        and then gets the neighbour node object by its position.
        The found values will be assigned to the neighbours list of the respective
        node object.
        """
        for node in self.nodes:
            node.neighbours = self.grid.get_neighbours_of_pos(node.pos)

        
    def get_node_by_pos(self, pos: tuple[int, int]) -> node.Node:
        """get_node_by_pos
        Returns a node object at the given position pos
        Params:
            * pos (tuple[int, int]): Position of the node that should be returned
        Returns:
            * (Node): Node object at the given position
        """
        for n in self.nodes:
            if n.pos == pos:
                return n
        return None
    
    

    def get_neighbours_of_node(self, node: node.Node) -> list[node.Node]:    
        """get_neighbours_of_node
        Get all neighbour nodes of a given node.
        Params:
            * node (Node): node in the graph from which you want the neighbours
        Returns:
            * (list[node.Node]): neighbours of the given node 
        """
        return self.adjac_list[node]
    
    
    def set_adjac_list(self):
        """set_adjac_list
        Initializes the adjac list of the graph with all nodes in the grid as keys and
        all of their neighbour nodes as their respective values.
        """
        for n in self.nodes:
            neighbour_nodes = []
            for key_dir in n.neighbours:
                pos = n.neighbours[key_dir]
                node = self.get_node_by_pos(pos)
                neighbour_nodes.append(node)
            self.adjac_list[n] = neighbour_nodes
            

    def get_sum(self, x, y):
        """get_sum
        Gets sum of two values
        
        Params:
            * x (float): x-position of a node
            * y (float): y-position of a node
        Returns:
            * (float): sum of two values
        """
        return x+y
    

    def h_score_cost_estimate(self, src_node: node.Node) -> float:
        """h_cost
        Calculates the estimated cost from current node to goal node with the manhatten metric.
        Calculation via following formula: |dstx - srcx| + |dsty - srcy|
        Params: 
            * src_node (Node): Node from which the distance to the dest node should be calculated
        Returns:
            * (float): manhattan distance between a node to the destination node
        """
        # set dest_node
        dest_node = self.end_node
        
        # set positions
        src_x = src_node.pos[0]
        dest_x = dest_node.pos[0]
        src_y = src_node.pos[1]
        dest_y = dest_node.pos[1]
        
        # set h_score of node
        h_score = self.get_sum(abs(dest_x - src_x), abs(dest_y - src_y))
        
        # returns h_score value by formula |dstx - srcx| + |dsty - srcy|
        return h_score



    def a_start_algorithm(self) -> list[tuple[int, int]]:
        """a_start_algorithm
        Find a best path solution from a source node to a destination node.
        The best path solution is the path with the lowest cost.
        Contains these steps:
            1 Start with the starting node in the open_list
            2 remove node from open_list when smallest f_score value
            3 append node to closed_list 
            4 if the node is the end node -> successful return
            5 else find all neighbours of the node
            6 calculate g-,h- and f-score values of the neighbour nodes
            8 append all neighbour nodes to the open_list
            7 GoTo step 2
            8 Exit  
        Returns:
            (list[tuple[int, int]]): best path solution as a list with position-tuples
        """
        # initializes open and closed list
        # open list contains nodes that hasn't been visited
        # either contains the neighbours of a visited node or is the start node
        # closed list contains already visited nodes
        open_list = []  
        closed_list = []  
        open_list.append(self.start_node)
        
        while len(open_list) > 0:
            curr_node = None
            for node in open_list:
                if curr_node == None or node.f_score < curr_node.f_score:
                    curr_node = node
            open_list.remove(curr_node)
            closed_list.append(curr_node)
            
            # when current node is none, path doesn't exist
            if curr_node == None:
                print('Path does not exist!')
                return None
            
            # if path to goal is found
            if curr_node == self.end_node:
                curr = curr_node
                while curr is not None:
                    self.best_path_solution.append(curr.pos)
                    curr = curr.parent
                # reverse so it contains pos-tuples from start to end
                self.best_path_solution.reverse()                  
                print("Path Found!")
                return self.best_path_solution
            
            # add neighbours to open list
            for neighbour_node in self.get_neighbours_of_node(curr_node):
                new_g_score_of_neighbour_node = curr_node.g_score + neighbour_node.cost

                # if neighbour node is not in open_list and closed_list -> add to open list
                # also set its parent
                # and its f, g and h scores
                if neighbour_node not in open_list and neighbour_node not in closed_list:
                    open_list.append(neighbour_node)
                    neighbour_node.parent = curr_node
                    neighbour_node.g_score = new_g_score_of_neighbour_node
                    neighbour_node.h_Score = self.h_score_cost_estimate(neighbour_node)
                    neighbour_node.f_score = neighbour_node.g_score + neighbour_node.h_Score
                
                # else: if neighbour node is in one of the lists
                # check if other path from current_node to neighbour_node is quicker
                # if yes: update parent data and score data
                # move neighbour node from closed to open list
                elif (neighbour_node in open_list) or (neighbour_node in closed_list) and (new_g_score_of_neighbour_node < neighbour_node.g_score):
                    neighbour_node.parent = curr_node
                    neighbour_node.g_score = new_g_score_of_neighbour_node
                    neighbour_node.h_Score = self.h_score_cost_estimate(neighbour_node)
                    neighbour_node.f_score = neighbour_node.g_score + neighbour_node.h_Score
                    
                    if neighbour_node in closed_list:
                        open_list.append(neighbour_node)
                        closed_list.remove(neighbour_node)
                        # update lists 
    
        print('Path does not exist!')
        return None    

    def show_best_path_solution_of_a_star(self) -> pd.DataFrame:
        """show_best_path_solution_of_a_star
        Applies the dataframe styling data on the grid dataframe.
        It returns a DataFrame with the best path solution that was 
        found by the a* algorithm.
        Returns:
            pd.DataFrame: DataFrame with colored best path solution
        """
        df = self.grid.df_grid.astype(int)
        return df.style.apply(self.styling_specific_cell, axis = None)  # Axis set to None to work on entire dataframe
    
    def styling_specific_cell(self, x) -> pd.DataFrame:
        """styling_specific_cell
        Returns a dataframe with colored cells that show the elements of the best path solution
        that was found by the a* algorithm.
        Params:
            x (pd.DataFrame): dataframe to be styled
        Returns:
            pd.DataFrame: DataFrame with styling data of the cells
        """
        color = 'background-color: orange; color: black'
        df_styler = pd.DataFrame('', index=x.index, columns=x.columns)
        for (x, y) in self.best_path_solution:
            df_styler.iloc[y, x] = color
        return df_styler
        
        
                


# H_COST and cost along axis -- do not use
    """h_cost
    Calculates the cost from current node to goal node with the manhatten metric.
    Calculation via following formula: |dstx - srcx| + |dsty - srcy|
    
    Returns:
        * (float): manhattan distance between a source node to the destination node
    """
    """
    def h_score_cost_estimate(self, src_node: node.Node, dest_node: node.Node) -> float:
        src_node = self.get_node_by_pos((0, 5))
        x_cost = self.get_cost_along_axis(src_node=src_node, dest_node=dest_node, axis="x")
        y_cost = self.get_cost_along_axis(src_node=src_node, dest_node=dest_node, axis="y")
        return x_cost + y_cost
    """ 
    
    """get_cost_along_axis
    Calculates the cost along a specific axis (x or y) from the src_node to the destination node.
    e.g.: Moving from src_node.pos -> end_node.pos: (0,0) -> (1, 1) along x-axis with cost 2 will deliver
    the value 2 for the x-axis.
    Params:
        * axis (str): along which axis the costs should be summed
        * src_node (Node): node from which it starts to sum up the costs
        * dest_node (Node): node from which it ends up summing up the costs
    Returns:
        * (float): the costs of moving along one axis from a source to a destination node
    """
    
    """
    def get_cost_along_axis(self, axis:str, src_node: node.Node, dest_node: node.Node) -> float:
        # set values depending on axis
        if(axis=="x"):
            src_axis = src_node.pos[0]
            dest_axis = dest_node.pos[0]
        else:
            src_axis = src_node.pos[1]
            dest_axis = dest_node.pos[1]
        
        # how many nodes to get the cost from
        dist_along_axis = dest_axis - src_axis
        
        # in case of no movement
        if(dist_along_axis == 0):
            return 0
        
        # conditions for determining the moving direction
        if(axis=="x"):
            if dist_along_axis > 0:
                direction = "right"
            else:
                direction = "left"
            curr_node = src_node
        else:
            if dist_along_axis < 0:
                direction = "up"
            else:
                direction = "down"
            curr_node = dest_node
        
        # summing up the costs along one axis
        costs_along_axis = 0        
        for i in range(abs(dist_along_axis)):
            if(axis == "x"):
                node_offset = self.get_node_by_pos(curr_node.neighbours[direction])
                curr_node = node_offset
                costs_along_axis = costs_along_axis + curr_node.cost
            else:
                curr_node = self.get_node_by_pos(curr_node.pos)
                costs_along_axis = costs_along_axis + curr_node.cost
                curr_node = self.get_node_by_pos(curr_node.neighbours[direction])
        return costs_along_axis
    """