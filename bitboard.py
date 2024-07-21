from typing import Optional


class BitBoard:
    """
    Bitboard class data class that contains information about the location of
    pieces on the chessboard. Also contains helper utility functions for common
    bitboard operations.

    Attributes:
        bitboard (int): Integer storing binary representation of a bitboard
    """

    def __init__(self, bitboard: Optional['BitBoard'] = None):
        if bitboard is not None:
            self.bitboard = bitboard.bitboard
        else:
            self.bitboard = int('0b0', 2)

    def __or__(self, bitboard: 'BitBoard') -> 'BitBoard':
        self.bitboard = self.bitboard | bitboard.bitboard
        return self.__copy__()

    def __and__(self, bitboard: 'BitBoard') -> 'BitBoard':
        self.bitboard = self.bitboard & bitboard.bitboard
        return self.__copy__()

    def __xor__(self, bitboard: 'BitBoard') -> 'BitBoard':
        self.bitboard = self.bitboard ^ bitboard.bitboard
        return self.__copy__()

    def __invert__(self, bitboard: 'BitBoard') -> 'BitBoard':
        self.bitboard = ~self.bitboard
        return self.__copy__()

    def __add__(self, bitboard: 'BitBoard') -> 'BitBoard':
        return self | bitboard

    def __sub__(self, bitboard: 'BitBoard') -> 'BitBoard':
        bitboard = self & bitboard
        return self ^ bitboard

    def __iadd__(self, bitboard: 'BitBoard') -> 'BitBoard':
        self = self | bitboard
        return self

    def __isub__(self, bitboard: 'BitBoard') -> 'BitBoard':
        # Remove any bits that are not present in 'self' bitboard
        bitboard = bitboard & self
        self = self ^ bitboard
        return self

    def __copy__(self):
        return BitBoard(self)

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

        if self.get(row, col):
            self.bitboard = self.bitboard ^ mask

    def get(self, row: int, col: int) -> int:
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

    def show(self):
        result = bin(self.bitboard)

        # Remove "0b" prefix
        result = result[2:]

        # Perform zero padding at the beginning of the bitboard
        result = "0" * (64-len(result)) + result

        # Reverse bitboard string (position 7, 7 is first position of bitboard)
        print("="*40)
        for i in range(8):
            print(result[8*i:8*i+8])
        print("="*40)

    def get_num_pieces(self) -> int:
        # Convert to binary string representation
        bin_str = bin(self.bitboard)
        return bin_str.count("1")


if __name__ == "__main__":
    bitboard = BitBoard()
    bitboard.set(4, 5)
    bitboard.set(3, 7)
    bitboard.unset(3, 7)
    bitboard.unset(0, 0)
    bitboard.set(4, 5)

    val = 1 << 63 - (8*4 + 5)
    assert bitboard.bitboard ^ val == 0

    bitboard_copy = BitBoard(bitboard)
    bitboard_copy.unset(4, 5)
    bitboard_copy.set(1, 3)
    bitboard_copy.set(3, 3)

    bitboard.show()
    bitboard_copy.show()

    bitboard += bitboard_copy
    bitboard.show()

    assert bitboard.get_num_pieces() == 3, f"{bitboard.get_num_pieces()}"
