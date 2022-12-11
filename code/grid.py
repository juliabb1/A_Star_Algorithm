import numpy as np
import os
import pandas as pd

class Grid():

    def __init__(self, csv_filename: str = "S_001_Daten.csv"):
        """Initializes the grid object.
        Sets the attribute values of the object.
        Params:
            * csv_filename (str): name of csv with data to extract from
        """
        self.df_grid = None
        self.np_grid = None
        self.pos_grid = None
        self.df_caption = None
        self.width = None
        self.height = None
        
        self.extract_data(csv_filename)
        self.set_pos_grid()
    
    
    def set_pos_grid(self) -> None:
        """set_pos_grid
        Sets a numpy array that contains each position of the grid as a tuple (x, y).
        """
        pos_grid = np.zeros(shape=self.np_grid.shape, dtype=tuple)
        for x in range(self.width):
            for y in range(self.height):
                pos_grid[x][y] = (x,y)
        self.pos_grid = pos_grid
    

    def extract_data(self, csv_filename) -> None: 
        """extract_data
        Extracts data from a csv file and configures the grid:
            - Constructs the landscape grid as np array.
            - Constructs the caption of the landscape as pd.dataframe.
            - Sets the start and end position. 
        Params: 
            * csv_filename (str): name of csv with data to extract from
        """
        path_to_csv = os.path.join(os.path.dirname( __file__ ), '..', "SEARCH_001", "S001", csv_filename)
        df_total = pd.read_csv(path_to_csv, sep=";", encoding="unicode-escape", header=None)

        # seperate the dataframe in three subdataframes
        ## df_landscape / np_landscape
        endrow_landscape_data = df_total.loc[pd.isna(df_total[0])].index[0]         # get index of a row containing NaN in column 0
        df_landscape = df_total[:endrow_landscape_data]                             # get landscape part of data
        df_landscape = df_landscape.astype(float) # clean data
        self.df_grid = df_landscape
        np_landscape = df_landscape.to_numpy().T    # to numpy
        self.np_grid = np_landscape
        
        ## df_caption
        startrow_caption_data = endrow_landscape_data + 1
        df_caption = pd.read_csv(path_to_csv, sep=";", encoding="unicode-escape", skiprows=startrow_caption_data, usecols=["Code", "Bezeichnung", "Kosten"])
        df_caption["Code"] = df_caption["Code"].astype(int)                         # clean data
        df_caption["Bezeichnung"] = df_caption["Bezeichnung"].astype(str)           # clean data
        df_caption["Kosten"] = df_caption["Kosten"].astype(float)                   # clean data
        self.df_caption = df_caption
        
        ## set width and height
        self.height = df_landscape.shape[0]
        self.width = df_landscape.shape[1]
        

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        """in_bounds
        Checks if a given position is in bounds of the grid.
        Params:
            * pos (tuple[int, int]): position to be checked if valid
        Returns:
            * (bool): true if pos is in bounds. false if not.
        """
        x = pos[0]
        y = pos[1]
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_code_of_pos(self, pos: tuple[int, int]) -> float:
        """get_code_of_pos
        Gets the code number of a specific position in the grid.
        Params:
            * pos (tuple[int, int]): position to get the code from
        Returns:
            * (float): code of the position
        """
        x = pos[0]
        y = pos[1]      
        return self.np_grid[x][y]
    

    def get_cost_of_pos(self, pos: tuple[int, int]) -> float:
        """get_cost_of_pos
        Gets the cost of a specific position in the grid.
        Params:
            * pos (tuple[int, int]): position to get the cost from
        Returns:
            * (float): cost of the position
        """
        code = self.get_code_of_pos(pos) 
        cost = self.df_caption.loc[self.df_caption["Code"] == code, "Kosten"].iloc[0]
        return cost


    def get_name_of_pos(self, pos: tuple[int, int]) -> str:
        """get_name_of_pos
        Gets the name of a specific position in the grid.
        Params:
            * pos (tuple[int, int]): position to get the name from
        Returns:
            * (str): name of the position
        """
        code = self.get_code_of_pos(pos) 
        name = self.df_caption.loc[self.df_caption["Code"] == code, "Bezeichnung"].iloc[0]
        return name
    

    def get_neighbours_of_pos(self, pos: tuple[int, int]) -> dict[str, tuple[int, int]]:
        """get_neighbours_of_pos
        Gets the position of the neighbours of a specific position in the grid.
        Neighbors are only the neighbors along the axes. Not diagonal.
        Params:
            * pos (tuple[int, int]): position to get the neighbours from
        Returns:
            * (list[tuple[int, int]]): list of positions that are neighbour posiitons of a given position
        """
        x = pos[0]
        y = pos[1]
        neighbours = {}
        
        # right
        right = (x+1, y)
        if(self.in_bounds(right)):
            neighbours["right"] = right
        # left
        left = (x-1, y)
        if(self.in_bounds(left)):
            neighbours["left"] = left
        # up
        up = (x, y+1)
        if(self.in_bounds(up)):
            neighbours["up"] = up
        # down
        down = (x, y-1)
        if(self.in_bounds(down)):
            neighbours["down"] = down
        return neighbours        
