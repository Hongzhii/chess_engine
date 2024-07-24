from typing import Tuple, Optional

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
