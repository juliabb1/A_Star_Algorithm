import node 
class Graph():
    """__init__
    Initializes Graph.
    
    Params:
        * adjac_list (list): adjacency list of graph
    """
    def __init__(self, adjac_list = {}):
        self.adjac_list = adjac_list
    
    def add_node_to_adjac_list(self, node, neighbor_nodes: list):
        self.adjac_list[node] = neighbor_nodes    
    
    """get_neighbours
    Gets nodes connected to the given node
    
    Params:
        * node (Node): node in the graph from which you want the neighbours
    Returns:
        * (Node): neighbours of the given node
    """
    def get_neighbours(self, node):
        return self.adjac_list[node]
    
    """get_sum
    Gets sum of two values
    
    Params:
        * x (float): x-position of a node
        * y (float): y-position of a node
    Returns:
        * (float): sum of two values
    """
    def get_sum(x, y):
        return x+y
    
    """h_cost
    Calculates the cost from current node to goal node with the manhatten metric.
    Calculation via following formula: |dstx - srcx| + |dsty - srcy|
    
    Returns:
        * (float): manhattan distance between a source node to the destination node
    """
    def h_score_cost_estimate(self, src, dest):
        # returns: |dstx - srcx| + |dsty - srcy|
        return sum(abs(dest[0] - src[0]), abs(dest[1], src[1]))
    
    def a_start_algorithm(self, start, stop):
        