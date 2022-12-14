class Node():
    """Class of a Node. Nodes are part of the graph.
    """
    
    def __init__(self, cost: float, pos: tuple[int, int], code: float, name: str):
        """__init__
        Initializes Node object.
        Params:
            * pos (tuple[int, int]):     position of the node (x, y)
            * cost (float):              cost of the node
            * code (float):              code of the node
            * name (str):                name of the node
        """
        # required
        self.pos = pos
        self.cost = cost
        self.code = code
        self.name = name
        
        # later to be adjusted
        self.neighbours = {}
        self.parent = None
        self.g_score = float("inf")              # costs between node and start node
        self.h_score = 0                         # heuristic value - (under)estimated costs between node and end node   
        self.f_score = float("inf")              # total cost of the node - f = g + h 
    