from board import Board
from bitboard import BitBoard
from typing import Tuple

class PieceHandler:
    """
    A class to retrieve all legal moves for a given piece on a board.

    Attributes:

    """
    def __init__(
        self,
        board: Board
    ):
        """
        Constructor for the piece handler class

        Args:
        board (Board): Board class object
        """
        self.board = board

    @staticmethod
    def _in_range(
        position: Tuple[int, int]
    ) -> bool:
        """
        Helper function to check if a given position is inside of a chessboard

        Args:
        position (Tuple[int, int]): Position of piece

        Returns:
        isValid (bool): Whether or not position is within chessboard
        """
        i_valid = 0 <= position[0] and position[0] <= 7
        j_valid = 0 <= position[1] and position[1] <= 7

        return i_valid and j_valid

    @classmethod
    def _get_pawn_bitboard(
        cls,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        bitboard = BitBoard()

        if color == -1:
            bitboard.set(max(position[0] - 1, 0), position[1])
            bitboard.set(max(position[0] - 2, 0), position[1])
        else:
            bitboard.set(min(position[0] + 1, 7), position[1])
            bitboard.set(min(position[0] + 2, 7), position[1])

        return bitboard
    
    @classmethod
    def _get_knight_bitboard(
        cls,
        position: Tuple[int, int]
    ) -> BitBoard:
        bitboard = BitBoard()

        candidate_locations = [
            (position[0] + 2, position[1] + 1),
            (position[0] + 2, position[1] - 1),
            (position[0] - 2, position[1] + 1),
            (position[0] - 2, position[1] - 1),
            (position[0] + 1, position[1] + 2),
            (position[0] - 1, position[1] + 2),
            (position[0] + 1, position[1] - 2),
            (position[0] - 1, position[1] - 2)
        ]

        for location in candidate_locations:
            if cls._in_range(location):
                bitboard.set(location[0], location[1])

        return bitboard
    
    @classmethod
    def _get_bishop_bitboard(
        cls,
        position: Tuple[int, int]
    ) -> BitBoard:
        bitboard = BitBoard()

        initial_position = position

        while True:
            position[0] += 1
            position[1] += 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[0] -= 1
            position[1] += 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[0] += 1
            position[1] -= 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[0] -= 1
            position[1] -= 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])


    @classmethod
    def _get_rook_bitboard(
        cls,
        position: Tuple[int, int]
    ) -> BitBoard:
        bitboard = BitBoard()

        initial_position = position

        while True:
            position[0] += 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[0] -= 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[1] += 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

        while True:
            position[1] -= 1

            if not cls._in_range(position):
                position = initial_position
                break

            bitboard.set(position[0], position[1])

    @classmethod
    def _get_queen_bitboard(
        cls,
        position: Tuple[int, int]
    ) -> BitBoard:
        bishop_component = cls._get_bishop_bitboard(position)
        rook_component = cls._get_rook_bitboard(position)

        
