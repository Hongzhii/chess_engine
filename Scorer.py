from typing import Dict
from my_types import Board

class Scorer:
    """
    Class that handles different types of board evaluation methods
    """
    
    def __init__(
        self,
        piece_values: dict
    ) -> None:
        self.piece_values = piece_values

    def _get_piece_value_score(
        self,
        board: Board
    ) -> float:
        score = 0

        # White pieces have positive scores
        for piece in board.white_positions:
            bitboard = board.white_positions[piece]
            score += bitboard.count() * self.piece_values[piece]

        # Black pieces have negative scores
        for piece in board.black_positions:
            bitboard = board.black_positions[piece]
            score -= bitboard.count() * self.piece_values[piece]

        return score
    
    def get_score(
        self,
        board: Board
    ) -> float:
        return self._get_piece_value_score(board)


from Board import Board

if __name__ == "__main__":
    piece_vals = {
        "p": 1.0,
        "n": 3.0,
        "b": 3.0,
        "r": 5.0,
        "q": 9.0,
        "k": 0.0
    }

    board = Board()
    scorer = Scorer(piece_vals)
    assert scorer.get_score(board) == 0
