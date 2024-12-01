from typing import Tuple, Optional

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
FILE_TO_NUM = {FILES[i]: i for i in range(len(FILES))}


def parse_algebraic(
    user_input: str,
    to_move: int,
    pieces: dict
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
        Simple movement (nf3, ke2, e4)
        Ambigous piece moves (nef3, n1f3, ref3, r1f3)
        Captures (exd5, nxf3, nexf3)
        Promotion (e8=q)
    """
    user_input = user_input.lower()
    user_input = user_input.strip()

    # Handle castling case
    if user_input == "o-o" and to_move == -1:
        return "k", (0, 4), (0, 6)
    elif user_input == "o-o" and to_move == 1:
        return "k", (7, 4), (7, 6)
    elif user_input == "o-o-o" and to_move == -1:
        return "k", (0, 4), (0, 2)
    elif user_input == "o-o-o" and to_move == 1:
        return "k", (7, 4), (7, 2)
    
    # Handle pawn moves
    if len(user_input) == 2:
        pass


def alphanumeric_to_index(position: str) -> Tuple[int, int]:
    """
    Helper function to turn positions from alphanumeric form to numerical
    index form

    Args:
        position (str): Position in alphanumeric form

    Returns:
        result (Tuple[int, int]): Position in index form
    """
    if position == "-":
        return None

    if len(position) != 2:
        raise ValueError(f"Invalid input {position} with input length: {len(position)}")

    file = position[0]
    rank = position[1]

    if file not in set("abcdefgh"):
        raise ValueError(f"Invalid file: {file}")
    if rank not in set("12345678"):
        raise ValueError(f"Invalid rank: {file}")

    assert file in set("abcdefgh")
    assert rank in set("12345678")

    file_no = FILE_TO_NUM[file]

    return (8 - int(rank), file_no)


if __name__ == "__main__":
    test1 = "a1"
    test2 = "A1"

    test3 = "f8"
    test4 = "e3"

    assert alphanumeric_to_index(test1) == (7, 0)
    assert alphanumeric_to_index(test2) == (7, 0)

    assert alphanumeric_to_index(test3) == (0, 5)
    assert alphanumeric_to_index(test4) == (5, 4)
