from typing import Tuple
from board import Board

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
FILE_TO_NUM = {FILES[i]: i for i in range(len(FILES))}


def parse_algebraic(
    user_input: str,
    board: Board
) -> Tuple[str, Tuple, Tuple]:
    """
    Helper function to parse algebraic chess notation and extract piece type
    and destination square information.

    Args:
        user_input (str): Algebraic chess notation string input

    Returns:
        A parsing result containing piece type information and starting, ending
        coordinates.

    Input cases:
        Castling (o-o, o-o-o)
        Simple movement (Nf3, Ke2, e4)
        Ambigous piece moves (Nef3, N1f3, Ref3, R1f3)
        Captures (exd5, Nxf3, Nexf3)
        Promotion (e8=q)
    """
    user_input = user_input.strip()

    # Handle castling case
    if user_input == "o-o" and board.to_move == -1:
        return "k", (0, 4), (0, 6)
    if user_input == "o-o" and board.to_move == 1:
        return "k", (7, 4), (7, 6)
    if user_input == "o-o-o" and board.to_move == -1:
        return "k", (0, 4), (0, 2)
    if user_input == "o-o-o" and board.to_move == 1:
        return "k", (7, 4), (7, 2)

    # Find the piece types
    if user_input[0] in set("NBRKQ"):
        piece_type = user_input[0]
    elif user_input[0] in set("abcdefgh"):
        piece_type = "P"
    else:
        raise ValueError(f"Invalid input: {user_input}")

    # Find the destination coordinates
    if "=" in user_input:  # Handle promotion cases
        end_square = user_input[:2]
    else:  # Handle all other cases
        end_square = user_input[-2:]

    if board.to_move == -1:
        piece_type = piece_type.lower()

    # Find coordinates of target piece

    # Find legal moves of target pieces

    return piece_type, end_square


def alphanumeric_to_index(position: str) -> Tuple[int, int]:
    """
    Helper function to turn positions from alphanumeric form to numerical
    index form

    Args:
        position (str): Position in alphanumeric form

    Returns:
        result (Tuple[int, int]): Position in index form

    Throws:
        ValueError: For alphanumeric coorinate inputs in invalid format
    """
    if position == "-":
        return None

    if len(position) != 2:
        raise ValueError(f"Invalid input {position} with input length: {len(position)}")

    file = position[0]
    rank = position[1]

    if file not in "abcdefgh":
        raise ValueError(f"Invalid column: {file}")
    if rank not in "12345678":
        raise ValueError(f"Invalid row: {file}")

    file_no = FILE_TO_NUM[file]

    return (8 - int(rank), file_no)
