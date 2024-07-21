from typing import Tuple

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
FILE_TO_NUM = {FILES[i]: i for i in range(len(FILES))}


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

    assert len(position) == 2, f"{position}"

    file = position[0]
    rank = position[1]

    assert file in set("abcdefgh")
    assert rank in set("12345678")

    file_no = FILE_TO_NUM[file]

    return (8 - int(rank), file_no)
