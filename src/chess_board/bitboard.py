from typing import Optional, List, Tuple


class BitBoard:
    """
    Bitboard class data class that contains information about the location of
    pieces on the chessboard. Also contains helper utility functions for common
    bitboard operations.

    Attributes:
        bitboard (int): Integer storing binary representation of a bitboard
    """

    def __init__(
        self,
        coordinates: Optional[List[Tuple[int, int]]] = None,
        bitboard: Optional['BitBoard'] = None
    ):
        if bitboard is not None:
            self.bitboard = bitboard.bitboard
        elif coordinates is not None:
            self.bitboard = int('0b0', 2)

            for coord in coordinates:
                try:
                    assert len(coord) == 2
                    assert 0 <= coord[0] and coord[0] <= 7
                    assert 0 <= coord[1] and coord[1] <= 7
                    self.set(coord[0], coord[1])
                except AssertionError:
                    print(f"Error: invalid coordinates {coord}, skipping...")
        else:
            self.bitboard = int('0b0', 2)

    def __eq__(self, bitboard: 'BitBoard') -> bool:
        return self.bitboard == bitboard.bitboard

    def __ne__(self, bitboard: 'BitBoard') -> bool:
        return self.bitboard != bitboard.bitboard

    def __or__(self, bitboard: 'BitBoard') -> 'BitBoard':
        temp_bitboard = self.__copy__()
        temp_bitboard.bitboard = self.bitboard | bitboard.bitboard
        return temp_bitboard

    def __and__(self, bitboard: 'BitBoard') -> 'BitBoard':
        temp_bitboard = self.__copy__()
        temp_bitboard.bitboard = self.bitboard & bitboard.bitboard
        return temp_bitboard

    def __xor__(self, bitboard: 'BitBoard') -> 'BitBoard':
        temp_bitboard = self.__copy__()
        temp_bitboard.bitboard = self.bitboard ^ bitboard.bitboard
        return temp_bitboard

    def __invert__(self) -> 'BitBoard':
        self.bitboard = ~self.bitboard
        return self.__copy__()

    def __add__(self, bitboard: 'BitBoard') -> 'BitBoard':
        return self | bitboard

    def __sub__(self, bitboard: 'BitBoard') -> 'BitBoard':
        return self ^ (self & bitboard)

    def __iadd__(self, bitboard: 'BitBoard') -> 'BitBoard':
        return self + bitboard

    def __isub__(self, bitboard: 'BitBoard') -> 'BitBoard':
        return self - bitboard

    def __copy__(self):
        return BitBoard(bitboard=self)

    def __str__(self) -> str:
        result = bin(self.bitboard)

        # Remove "0b" prefix
        result = result[2:]

        # Perform zero padding at the beginning of the bitboard
        result = "0" * (64-len(result)) + result

        return_string = ""

        # Reverse bitboard string (position 7, 7 is first position of bitboard)
        return_string += F"{'='*40}\n"
        for i in range(8):
            return_string += f"{result[8*i:8*i+8]}\n"
        return_string += F"{'='*40}\n"

        return return_string

    def set(self, row: int, col: int) -> None:
        """
        Sets location specified. If specified location is already occupied,
        do nothing.

        Args:
            row (int): Specified row
            col (int): Specified column
        """
        position = row * 8 + col

        # row 7 col 7 is actually first position on the bitboard
        position = 63 - position
        assert position >= 0, f"Got position: {position}"

        mask = 1 << position

        self.bitboard = self.bitboard | mask

    def unset(self, row: int, col: int) -> None:
        """
        Unsets location specified. If specified location is already empty,
        do nothing.

        Args:
            row (int): Specified row
            col (int): Specified column
        """
        position = row * 8 + col

        # row 7 col 7 is actually first position on the bitboard
        position = 63 - position
        assert position >= 0

        mask = 1 << position

        if self.is_occupied(row, col):
            self.bitboard = self.bitboard ^ mask

    def is_occupied(self, row: int, col: int) -> int:
        """
        Gets value at specified location.

        Args:
            row (int): Specifed row
            col (int): Specified column

        Returns:
            result (int): 1 for occupied, 0 for empty
        """
        position = row * 8 + col

        # row 7 col 7 is actually first position on the bitboard
        position = 63 - position
        assert position >= 0

        mask = 1 << position

        return (mask & self.bitboard) >> position

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        Returns a list of coordinates representing all positions on the bitboard.

        Args:
            None

        Returns:
            result (List[Tuple[int, int]]): List of coordinate tuples
        """
        string_rep = bin(self.bitboard)[2:]
        string_rep = (64 - len(string_rep)) * "0" + string_rep  # Re-add the leading zeros

        result = []

        for i, char in enumerate(string_rep):
            if char == "1":
                result.append((i//8, i%8))

        return [(i//8, i%8) for i, char in enumerate(string_rep) if char == "1"]

    def count(self) -> int:
        """
        Counts the number of pieces present on the bitboard
        """
        bin_str = bin(self.bitboard)
        return bin_str.count("1")
