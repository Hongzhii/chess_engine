class BitBoard:
    def __init__(self):
        self.bitboard = int('0b0', 2)

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
        assert position >= 0

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
        for i in range(8):
            print(result[8*i:8*i+8])


if __name__ == "__main__":
    bitboard = BitBoard()
    bitboard.set(4, 5)
    bitboard.set(3, 7)
    bitboard.unset(3, 7)
    bitboard.unset(0, 0)
    bitboard.set(4, 5)

    val = 1 << 63 - (8*4 + 5)
    assert bitboard.bitboard ^ val == 0

    bitboard.print()
