import numpy as np

class Board:
    """
    A class to represent any given game state.

    Attributes:
        to_move (int): The player to move next. (1 or -1)
        board (np.array): A 2D array representing the game state.
    """

    
    @property
    def to_move(self):
        pass