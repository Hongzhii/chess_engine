from __future__ import annotations
from typing import Tuple
from src.bitboard import BitBoard

# from resources.my_types import Board, BitBoard

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


def get_pawn_moves(
    board: Board,
    position: Tuple[int, int],
    captures_only: bool = False,  # Moves do not imply captures for pawns
) -> BitBoard:
    piece = board.get_piece(position[0], position[1])
    if board.board_state["to_move"] == -1:
        assert piece == 'p', f"Got {piece}"
    else:
        assert piece == 'P', f"Got {piece}"

    bitboard = BitBoard()

    all_pieces = board.get_color_bitboard(1) + board.get_color_bitboard(-1)

    if board.board_state["to_move"] == -1:
        if not all_pieces.is_occupied(position[0] + 1, position[1]):
            bitboard.set(position[0] + 1, position[1])

        if position[0] == 1 and \
                not all_pieces.is_occupied(position[0] + 2, position[1]):
            bitboard.set(position[0] + 2, position[1])
    else:
        if not all_pieces.is_occupied(position[0] - 1, position[1]):
            bitboard.set(position[0] - 1, position[1])

        if position[0] == 6 and \
                not all_pieces.is_occupied(position[0] - 2, position[1]):
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

    if captures_only:
        return capture_bitboard

    bitboard += capture_bitboard

    return bitboard


def get_knight_moves(
    board: Board,
    position: Tuple[int, int],
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


def get_bishop_moves(
    board: Board,
    position: Tuple[int, int],
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

                if friendly_bitboard.is_occupied(row_index, col_index):
                    break

                bitboard.set(row_index, col_index)

                if opponent_bitboard.is_occupied(row_index, col_index):
                    break

    return bitboard


def get_rook_moves(
    board: Board,
    position: Tuple[int, int],
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

            if friendly_bitboard.is_occupied(index, position[1]):
                break

            bitboard.set(index, position[1])

            if opponent_bitboard.is_occupied(index, position[1]):
                break

        index = position[1]
        while True:
            index += i

            if not _in_range(position[0], index):
                break

            if friendly_bitboard.is_occupied(position[0], index):
                break

            bitboard.set(position[0], index)

            if opponent_bitboard.is_occupied(position[0], index):
                break

    return bitboard


def get_queen_moves(
    board: Board,
    position: Tuple[int, int],
) -> BitBoard:
    if board.board_state["to_move"] == -1:
        assert board.get_piece(position[0], position[1]) == 'q'
    else:
        assert board.get_piece(position[0], position[1]) == 'Q'

    bishop_component = get_bishop_moves(board, position)
    rook_component = get_rook_moves(board, position)

    return bishop_component + rook_component


def get_king_moves(
    board: Board,
    position: Tuple[int, int],
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
                and not friendly_bitboard.is_occupied(location[0], location[1]):
            bitboard.set(location[0], location[1])

    # Handle castling moves:
    if board.in_check() or board.board_state["castling"] == "-":
        return bitboard

    opponent_target_bitboard = board.in_check(return_target_bitboard=True)
    combined_pieces = board.get_color_bitboard(1) + board.get_color_bitboard(-1)

    if board.board_state["castling"][0] == "K" and board.board_state["to_move"] == 1:
        blocked = False
        targeted = False

        for col_num in [5, 6]:
            if combined_pieces.is_occupied(7, col_num):
                blocked = True
                break
            if opponent_target_bitboard.is_occupied(7, col_num):
                targeted = True
                break

        if not (blocked or targeted):
            bitboard.set(7, 6)

    if board.board_state["castling"][1] == "Q" and board.board_state["to_move"] == 1:
        blocked = False
        targeted = False

        for col_num in [1, 2, 3]:
            if combined_pieces.is_occupied(7, col_num):
                blocked = True
                break
            if opponent_target_bitboard.is_occupied(7, col_num) and col_num != 1:
                targeted = True
                break

        if not (blocked or targeted):
            bitboard.set(7, 2)

    if board.board_state["castling"][2] == "k" and board.board_state["to_move"] == -1:
        blocked = False
        targeted = False

        for col_num in [5, 6]:
            if combined_pieces.is_occupied(0, col_num):
                blocked = True
                break
            if opponent_target_bitboard.is_occupied(0, col_num):
                targeted = True
                break

        if not (blocked or targeted):
            bitboard.set(0, 6)
    
    if board.board_state["castling"][3] == "q" and board.board_state["to_move"] == -1:
        blocked = False
        targeted = False

        for col_num in [1, 2, 3]:
            if combined_pieces.is_occupied(0, col_num):
                blocked = True
                break
            if opponent_target_bitboard.is_occupied(0, col_num) and col_num != 1:
                targeted = True
                break

        if not (blocked or targeted):
            bitboard.set(0, 2)

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
        return get_pawn_moves(board, position)
    if piece_type.lower() == "n":
        return get_knight_moves(board, position)
    if piece_type.lower() == "b":
        return get_bishop_moves(board, position)
    if piece_type.lower() == "r":
        return get_rook_moves(board, position)
    if piece_type.lower() == "q":
        return get_queen_moves(board, position)
    return get_king_moves(board, position)
