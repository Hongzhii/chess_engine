from __future__ import annotations

from typing import Dict

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
