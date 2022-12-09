import numpy as np
import os
import pandas as pd

class Grid():
    """Initializes the grid object.
    Sets the attribute values of the object.
    Params:
        * csv_filename (str): name of csv with data to extract from
    """
    def __init__(self, csv_filename: str = "S_001_Daten.csv"):
        self.np_grid = None
        self.pos_grid = None
        self.df_caption = None
        self.start_pos = None
        self.end_pos = None
        self.width = None
        self.height = None
        
        self.extract_data(csv_filename)
        self.get_pos_grid()
    
    def get_pos_grid(self):
        pos_grid = np.zeros(shape=self.np_grid.shape, dtype=object)
        for x in range(self.width):
            for y in range(self.height):
                pos_grid[x][y] = (x,y)
        self.pos_grid = pos_grid
    
    """extract_data
    Extracts data from a csv file and configures the grid:
        - Constructs the landscape grid as np array.
        - Constructs the caption of the landscape as pd.dataframe.
        - Sets the start and end position. 
    Params: 
        * csv_filename (str): name of csv with data to extract from
    """
    def extract_data(self, csv_filename) -> None: 
        path_to_csv = os.path.join("SEARCH_001", "S001", csv_filename)
        df_total = pd.read_csv(path_to_csv, sep=";", encoding="unicode-escape", header=None)

        # seperate the dataframe in three subdataframes
        ## df_landscape / np_landscape
        endrow_landscape_data = df_total.loc[pd.isna(df_total[0])].index[0]         # get index of a row containing NaN in column 0
        df_landscape = df_total[:endrow_landscape_data]                             # get landscape part of data
        df_landscape = df_landscape.astype(float)                                   # clean data
        np_landscape = df_landscape.to_numpy().T                                    # to numpy
        self.np_grid = np_landscape
        
        ## df_caption
        startrow_caption_data = endrow_landscape_data + 1
        endrow_caption_data = df_total.loc[pd.isna(df_total[0])].index[1]            # get index of a row containing NaN in column 0
        nrows_caption_data = endrow_caption_data - startrow_caption_data - 1
        df_caption = pd.read_csv(path_to_csv, sep=";", encoding="unicode-escape", skiprows=startrow_caption_data, nrows=nrows_caption_data, usecols=["Code", "Bezeichnung", "Kosten"])
        df_caption["Code"] = df_caption["Code"].astype(int)                         # clean data
        df_caption["Bezeichnung"] = df_caption["Bezeichnung"].astype(str)           # clean data
        df_caption["Kosten"] = df_caption["Kosten"].astype(float)                   # clean data
        self.df_caption = df_caption

        ## df_start_end_pos
        startrow_pos_data = endrow_caption_data + 1                                             # get index of a row where start and endpoint information starts
        df_start_end_pos = pd.read_csv(path_to_csv, sep=";", encoding="unicode-escape", skiprows=startrow_pos_data, usecols=["Startpunkt", "Endpunkt"])
        df_start_end_pos.index = ["x", "y"]                                                     # transform dataframe
        df_start_end_pos["Startpunkt"] = df_start_end_pos["Startpunkt"].astype(int)             # clean data
        df_start_end_pos["Endpunkt"] = df_start_end_pos["Endpunkt"].astype(int)                 # clean data
        np_start_end_pos = df_start_end_pos.to_numpy().T                                        # to numpy
        self.start_pos = tuple(map(tuple, np_start_end_pos))[0]
        self.end_pos = tuple(map(tuple, np_start_end_pos))[1]
        
        ## set width and height
        self.height = df_landscape.shape[0]
        self.width = df_landscape.shape[1]
        
    """in_bounds
    Checks if a given position is in bounds of the grid.
    Params:
        * pos (tuple[int, int]): position to be checked if valid
    Returns:
        * (bool): true if pos is in bounds. false if not.
    """
    def in_bounds(self, pos: tuple[int, int]) -> bool:
        x = pos[0]
        y = pos[1]
        return 0 <= x < self.width and 0 <= y < self.height
    
    """get_code_of_pos
    Gets the code number of a specific position in the grid.
    Params:
        * pos (tuple[int, int]): position to get the code from
    Returns:
        * (float): code of the position
    """
    def get_code_of_pos(self, pos: tuple[int, int]) -> float:
        x = pos[0]
        y = pos[1]      
        return self.np_grid[x][y]
    
    """get_cost_of_pos
    Gets the cost of a specific position in the grid.
    Params:
        * pos (tuple[int, int]): position to get the cost from
    Returns:
        * (float): cost of the position
    """
    def get_cost_of_pos(self, pos: tuple[int, int]) -> float:
        code = self.get_code_of_pos(pos) 
        cost = self.df_caption.loc[self.df_caption["Code"] == code, "Kosten"].iloc[0]
        return cost

    """get_name_of_pos
    Gets the name of a specific position in the grid.
    Params:
        * pos (tuple[int, int]): position to get the name from
    Returns:
        * (str): name of the position
    """
    def get_name_of_pos(self, pos: tuple[int, int]) -> str:
        code = self.get_code_of_pos(pos) 
        name = self.df_caption.loc[self.df_caption["Code"] == code, "Bezeichnung"].iloc[0]
        return name
    
    """get_neighbours_of_pos
    Gets the position of the neighbours of a specific position in the grid.
    Neighbors are only the neighbors along the axes. Not diagonal.
    Params:
        * pos (tuple[int, int]): position to get the neighbours from
    Returns:
        * (list[tuple[int, int]]): list of positions that are neighbour posiitons of a given position
    """
    def get_neighbours_of_pos(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        x = pos[0]
        y = pos[1]
        neighbours = []
        
        # right
        right = (x+1, y)
        if(self.in_bounds(right)):
            neighbours.append((x+1, y))
        # left
        left = (x-1, y)
        if(self.in_bounds(left)):
            neighbours.append(left)
        # up
        up = (x, y+1)
        if(self.in_bounds(up)):
            neighbours.append(up)
        # down
        down = (x, y-1)
        if(self.in_bounds(down)):
            neighbours.append(down)
        return neighbours        