class Node():
    
    """__init__
    Initializes Node object.
    
    Params:
        * pos (tuple[int, int]):     position of the node [x, y]
        * cost (float):              cost of the node
        * code (float):              cost of the node
        * name (str):                cost of the node
    """
    def __init__(self, cost: float, pos: tuple[int, int], code: float, name: str):
        # required
        self.pos = pos
        self.cost = cost
        self.code = code
        self.name = name
        
        # later to be adjusted
        self.parent = None
        self.g = None            
        self.h = None            
        self.f_score = None
        
        