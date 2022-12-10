import node 
import grid

class Graph():
    """__init__
    Initializes Graph.
    
    Params:
        * grid (Grid): grid object that has been constructed by the extracted data
    """
    def __init__(self, grid: grid.Grid):
        self.grid = grid
        self.start_node = None
        self.end_node = None
        self.nodes = []
        self.adjac_list = {}
        
        self.set_nodes()
        self.set_start_end_nodes()
        self.set_adjac_list()

    """set_start_end_nodes
    Initializes the start and end node for the path finding.
    """
    def set_start_end_nodes(self):
        self.start_node = self.get_node_by_pos(self.grid.start_pos)
        self.end_node = self.get_node_by_pos(self.grid.end_pos)
    
    """set_nodes
    Initializes for every position in the grid a node object and adds it to the
    nodes-list of the graph. Also assigns all neighbour nodes to each node
    """
    def set_nodes(self):
        for x_row in self.grid.pos_grid:
            for pos_el in x_row:
                code = self.grid.get_code_of_pos(pos_el)
                cost = self.grid.get_cost_of_pos(pos_el)
                name = self.grid.get_name_of_pos(pos_el)
                n = node.Node(cost=cost, code=code, name=name, pos=pos_el)
                self.nodes.append(n)
        self.assign_neighbours_to_nodes()
    
    """assign_neighbours_to_nodes
    Assigns the neighbour nodes to each node.
    For that it iterates through all available nodes.
    It gets the position of the neighbour nodes of each node
    and then gets the neighbour node object by its position.
    The found values will be assigned to the neighbours list of the respective
    node object.
    """
    def assign_neighbours_to_nodes(self):
        for node in self.nodes:
            node.neighbours = self.grid.get_neighbours_of_pos(node.pos)

        
    """get_node_by_pos
    Returns a node object at the given position pos
    Params:
        * pos (tuple[int, int]): Position of the node that should be returned
    Returns:
        * (Node): Node object at the given position
    """
    def get_node_by_pos(self, pos: tuple[int, int]) -> node.Node:
        for n in self.nodes:
            if n.pos == pos:
                return n
        return None
    
    
    """get_neighbours_of_node
    Get all neighbour nodes of a given node.
    Params:
        * node (Node): node in the graph from which you want the neighbours
    Returns:
        * (Node): neighbours of the given node
    """
    def get_neighbours_of_node(self, node: node.Node) -> dict[node.Node, dict[str, list[node.Node]]]:
        return self.adjac_list[node]
    
    
    """set_adjac_list
    Initializes the adjac list of the graph with all nodes in the grid as keys and
    all of their neighbour nodes as their respective values.
    """
    def set_adjac_list(self):
        for n in self.nodes:
            neighbour_nodes = []
            for key_dir in n.neighbours:
                pos = n.neighbours[key_dir]
                node = self.get_node_by_pos(pos)
                neighbour_nodes.append(node)
            self.adjac_list[n] = neighbour_nodes
            

    """get_sum
    Gets sum of two values
    
    Params:
        * x (float): x-position of a node
        * y (float): y-position of a node
    Returns:
        * (float): sum of two values
    """
    def get_sum(awlf, x, y):
        return x+y
    
    """h_cost
    Calculates the cost from current node to goal node with the manhatten metric.
    Calculation via following formula: |dstx - srcx| + |dsty - srcy|
    
    Returns:
        * (float): manhattan distance between a source node to the destination node
    """
    def h_score_cost_estimate(self, src_node: node.Node, dest_node: node.Node) -> float:
        src_x = src_node.pos[0]
        dest_x = dest_node.pos[0]
        
        src_y = src_node.pos[1]
        dest_y = dest_node.pos[1]
        # returns: |dstx - srcx| + |dsty - srcy|
        print(abs(dest_x - src_x))
        print(abs(dest_y - src_y))
        return self.get_sum(abs(dest_x - src_x), abs(dest_y - src_y))

import node
import graph
import grid

    # Testing the h_score_cost_estimate function
if __name__ == '__main__':
    landscape = grid.Grid()
    g = graph.Graph(grid=landscape)
    src_node = g.get_node_by_pos((0,0))
    dest_node = g.get_node_by_pos((14,0))
    dist = g.h_score_cost_estimate(src_node=src_node, dest_node=dest_node)
    print(dist)


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