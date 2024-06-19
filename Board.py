import numpy as np
from Pieces import *

"""
-------------------------
|BR|BN|BB|BQ|BK|BB|BN|BR|
-------------------------
|BP|BP|BP|BP|BP|BP|BP|BP|
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|WP|WP|WP|WP|WP|WP|WP|WP|
-------------------------
|WR|WN|WB|WQ|WK|WB|WN|WR|
-------------------------
"""

class Board:
    """
    A class to represent any given game state.

    Attributes:
        to_move (int): The player to move next. (1 or -1)
        board (np.array): A 2D array representing the game state.
    """

    def __init__(self, fen_string: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = np.full((8, 8), None)

        if fen_string is None:
            # Setup default starting position
            self.to_move = 1
            pass

    def parse_fen(self, fen_string: str) -> np.ndarray:
        components = fen_string.split(" ")

        if(len(components) != 6):
            raise ValueError(f"Invalid FEN string, expected 6 components instead got {len(components)}")
        
        self.to_move = components[1]
        self.castling = components[2]
        self.en_passant = components[3]
        self.fifty_move = components[4]
        self.moves = components[5]

    def show_board(self) -> None:
        print("-" * 25)
        for row in self.board:
            for piece in row:
                if piece is None:
                    print("|  ", end = "")
                elif isinstance(piece, Pawn):
                    if piece.color == 1:
                        print("|WP", end = "")
                    else:
                        print("|BP", end = "")
                elif isinstance(piece, Knight):
                    if piece.color == 1:
                        print("|WN", end = "")
                    else:
                        print("|BN", end = "")
                elif isinstance(piece, Bishop):
                    if piece.color == 1:
                        print("|WB", end = "")
                    else:
                        print("|BB", end = "")
                elif isinstance(piece, Rook):
                    if piece.color == 1:
                        print("|WR", end = "")
                    else:
                        print("|BR", end = "")
                elif isinstance(piece, Queen):
                    if piece.color == 1:
                        print("|WQ", end = "")
                    else:
                        print("|BQ", end = "")
                elif isinstance(piece, King):
                    if piece.color == 1:
                        print("|WK", end = "")
                    else:
                        print("|BK", end = "")
            print("|")
            print("-" * 25)

    @property
    def to_move(self) -> int:
        """Get current player move"""
        return self._to_move
    
    @to_move.setter
    def to_move(self, player: str) -> None:
        if player not in {"w", "b"}:
            raise ValueError(
                "Player value should be either w or b\n" + 
                f"Got unexpected value: {player}"
            )
        else:
            self._to_move = -1 if player == "b" else 1

    @property
    def castling(self) -> str:
        return self._castling
    
    @castling.setter
    def castling(self, state: str) -> None:
        if state not in {
            "----", "---q", "--k-", "--kq", 
            "-Q--", "-Q-q", "-Qk-", "-Qkq", 
            "K---", "K--q", "K-k-", "K-kq",
            "KQ--", "KQ-q", "KQk-", "KQkq"
            }:
            raise ValueError(f"Invalid castling state: {state}")
        else:
            self._castling = state

    @property
    def en_passant(self) -> str:
        return self._en_passant
    
    @en_passant.setter
    def en_passant(self, state: str) -> None:
        if(state == "-"):
            self._en_passant = state
        elif len(state) != 2:
            raise ValueError(f"Invalid en passant string length, expected length 2 but got string: {state}")
        elif (state[0] not in set("abcdefgh") or state[1] not in set("12345678")):
            raise ValueError(f"Invalid en passant string: {state}")
        else:
            self._en_passant = state

    @property
    def fifty_move(self) -> int:
        return self._fifty_move
    
    @fifty_move.setter
    def fifty_move(self, num_moves: int) -> None:
        if(not isinstance(num_moves, int) or int < 0):
            raise ValueError(f"Expected non-negative integer for 'fifty_move', instead got: {num_moves}")
        else:
            self._fifty_move = num_moves

    @property
    def moves(self) -> int:
        return self._moves
    
    @moves.setter
    def moves(self, num_moves:int):
        if(not isinstance(num_moves, int) or int < 1):
            raise ValueError(f"Expected positive integer for 'moves', instead got: {num_moves}")
        else:
            self._moves = num_moves