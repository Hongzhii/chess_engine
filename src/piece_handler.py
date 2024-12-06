from typing import Tuple

from src.bitboard import BitBoard
from resources.my_types import Board

"""
File containing helper funcitons to retrieve legal moves for a given piece on a board
"""

def _in_range(
    row: int,
    col: int
) -> bool:
    """
    Helper function to check if a given position is inside of a chessboard

    Args:
    row (int): Row index of piece
    col(int): Column index of piece

    Returns:
    isValid (bool): Whether or not position is within chessboard
    """
    i_valid = 0 <= row <= 7
    j_valid = 0 <= col <= 7

    return i_valid and j_valid


def _get_pawn_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    piece = board.get_piece(position[0], position[1])
    if board.board_state["to_move"] == -1:
        assert piece == 'p', f"Got {piece}"
    else:
        assert piece == 'P', f"Got {piece}"

    bitboard = BitBoard()

    all_pieces = board.get_color_bitboard(1) + board.get_color_bitboard(-1)

    if board.board_state["to_move"] == -1:
        if not all_pieces.get(position[0] + 1, position[1]):
            bitboard.set(position[0] + 1, position[1])

        if position[0] == 1 and \
                not all_pieces.get(position[0] + 2, position[1]):
            bitboard.set(position[0] + 2, position[1])
    else:
        if not all_pieces.get(position[0] - 1, position[1]):
            bitboard.set(position[0] - 1, position[1])

        if position[0] == 6 and \
                not all_pieces.get(position[0] - 2, position[1]):
            bitboard.set(position[0] - 2, position[1])

    # List possible captures
    if board.board_state["to_move"] == -1:
        candidate_locations = [
            (position[0] + 1, position[1] + 1),
            (position[0] + 1, position[1] - 1)
        ]
    else:
        candidate_locations = [
            (position[0] - 1, position[1] + 1),
            (position[0] - 1, position[1] - 1)
        ]

    capture_bitboard = BitBoard()

    for location in candidate_locations:
        if _in_range(location[0], location[1]):
            capture_bitboard.set(location[0], location[1])

    # Check if opponent pieces exist on capture square
    opponent_bitboard = board.get_color_bitboard(board.board_state["to_move"] * -1)
    opponent_bitboard += board.board_state["en_passant"]  # Add en-passant captures

    capture_bitboard = capture_bitboard & opponent_bitboard

    bitboard += capture_bitboard

    return bitboard


def _get_knight_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) == 'n'
    else:
        assert board.get_piece(position[0], position[1]) == 'N'

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
        if _in_range(location[0], location[1]):
            bitboard.set(location[0], location[1])

    # Check if knight is attacking friendly pieces
    friendly_bitboard = board.get_color_bitboard(board.board_state["to_move"])
    friendly_bitboard = friendly_bitboard & bitboard

    bitboard = bitboard ^ friendly_bitboard

    return bitboard


def _get_bishop_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) in set("bq")
    else:
        assert board.get_piece(position[0], position[1]) in set("BQ")

    bitboard = BitBoard()

    friendly_bitboard = board.get_color_bitboard(board.board_state["to_move"])
    opponent_bitboard = board.get_color_bitboard(board.board_state["to_move"] * -1)

    for i in [-1, 1]:
        for j in [-1, 1]:
            row_index = position[0]
            col_index = position[1]
            while True:
                row_index += i
                col_index += j

                if not _in_range(row_index, col_index):
                    break

                if friendly_bitboard.get(row_index, col_index):
                    break

                bitboard.set(row_index, col_index)

                if opponent_bitboard.get(row_index, col_index):
                    break

    return bitboard


def _get_rook_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) in set("rq")
    else:
        assert board.get_piece(position[0], position[1]) in set("RQ")

    bitboard = BitBoard()

    friendly_bitboard = board.get_color_bitboard(board.board_state["to_move"])
    opponent_bitboard = board.get_color_bitboard(board.board_state["to_move"] * -1)

    for i in [-1, 1]:
        index = position[0]
        while True:
            index += i

            if not _in_range(index, position[1]):
                break

            if friendly_bitboard.get(index, position[1]):
                break

            bitboard.set(index, position[1])

            if opponent_bitboard.get(index, position[1]):
                break

        index = position[1]
        while True:
            index += i

            if not _in_range(position[0], index):
                break

            if friendly_bitboard.get(position[0], index):
                break

            bitboard.set(position[0], index)

            if opponent_bitboard.get(position[0], index):
                break

    return bitboard


def _get_queen_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) == 'q'
    else:
        assert board.get_piece(position[0], position[1]) == 'Q'

    bishop_component = _get_bishop_moves(board, position)
    rook_component = _get_rook_moves(board, position)

    return bishop_component + rook_component


def _get_king_moves(
    board: Board,
    position: Tuple[int, int]
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) == 'k'
    else:
        assert board.get_piece(position[0], position[1]) == 'K'

    bitboard = BitBoard()

    candidate_locations = [
        (position[0] + 1, position[1]),
        (position[0] - 1, position[1]),
        (position[0], position[1] + 1),
        (position[0], position[1] - 1),
        (position[0] + 1, position[1] + 1),
        (position[0] + 1, position[1] - 1),
        (position[0] - 1, position[1] + 1),
        (position[0] - 1, position[1] - 1),
    ]

    friendly_bitboard = board.get_color_bitboard(board.board_state["to_move"])

    for location in candidate_locations:
        if _in_range(location[0], location[1]) \
                and not friendly_bitboard.get(location[0], location[1]):
            bitboard.set(location[0], location[1])

    return bitboard


def get_moves(
    board: Board,
    position: Tuple[int, int],
    piece_type: str
) -> BitBoard:
    """
    Returns a bitboard of moves taking into account captures and
    friendly pieces

    Args:
        board (Board): Board state information
        position (Tuple[int, int]): Position of piece being moved
        piece_type (str): Piece being moved
    """
    assert piece_type in set("pnbrqk")

    if piece_type.lower() == "p":
        return _get_pawn_moves(board, position)
    if piece_type.lower() == "n":
        return _get_knight_moves(board, position)
    if piece_type.lower() == "b":
        return _get_bishop_moves(board, position)
    if piece_type.lower() == "r":
        return _get_rook_moves(board, position)
    if piece_type.lower() == "q":
        return _get_queen_moves(board, position)
    return _get_king_moves(board, position)


def in_check(
    board: Board
) -> bool:
    pass

# if __name__ == "__main__":
#     handler = PieceHandler()
#     print("======EN PASSANT TEST CASE======")
#     board = Board(FENs.ENPASSANT_FEN)
#     board.show()

#     print("Pawn Moves:")
#     print("(En-passant pawn)")
#     handler.get_moves(board, (3, 4), "P").show()

#     print("======FOUR KNIGHTS TESTCASE======")
#     board = Board(FENs.FOURKNIGHTS_FEN)
#     board.show()
#     print("Knight Moves:")
#     handler.get_moves(board, (5, 5), "N").show()
#     handler.get_moves(board, (5, 2), "N").show()
#     handler.get_moves(board, (2, 5), "n").show()
#     handler.get_moves(board, (2, 2), "n").show()

#     print("Bishop Moves:")
#     handler.get_moves(board, (7, 5), "B").show()
#     handler.get_moves(board, (7, 2), "B").show()
#     handler.get_moves(board, (0, 5), "b").show()
#     handler.get_moves(board, (0, 2), "b").show()

#     print("Queen Moves:")
#     handler.get_moves(board, (7, 3), "Q").show()
#     handler.get_moves(board, (0, 3), "q").show()

#     print("King Moves:")
#     handler.get_moves(board, (7, 4), "K").show()
#     handler.get_moves(board, (0, 4), "k").show()
