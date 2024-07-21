import numpy as np
from bitboard import BitBoard

"""
-----------------
|R|N|B|Q|K|B|N|R|
-------------------------
|BP|BP|BP|BP|BP|BP|BP|BP|
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|  |  |  |  |  |  |  |  |
-------------------------
|WP|WP|WP|WP|WP|WP|WP|WP|
-------------------------
|WR|WN|WB|WQ|WK|WB|WN|WR|
-------------------------
"""
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Board:
    """
    A class to represent any given game state.

    Attributes:
        to_move (int): The player to move next. (1 or -1)
        castling (str): KQkq type string to specify King/Queenside castling
        en_passant (str): Specify En-Passant capturable square
        fifty_move (int): Number of moves since last capture/pawn advance
        moves (int): Number of moves in total
        black_positions (dict): Stores bitboards for all black pieces
        white_positions (dict): Stores bitboards for all white pieces
    """

    def __init__(
        self,
        fen_string: str = STARTING_FEN
    ):
        """
        Constructor for the Board class by parsing FEN string

        Args:
            fen_string (str): FEN string representing the board state
        """

        self.black_positions = {
            "p": BitBoard(),
            "n": BitBoard(),
            "b": BitBoard(),
            "r": BitBoard(),
            "q": BitBoard(),
            "k": BitBoard()
        }

        self.white_positions = {
            "p": BitBoard(),
            "n": BitBoard(),
            "b": BitBoard(),
            "r": BitBoard(),
            "q": BitBoard(),
            "k": BitBoard()
        }

        components = fen_string.split(" ")

        if len(components) != 6:
            raise ValueError(f"Invalid FEN string, expected 6 components instead got {len(components)}")

        self.to_move = components[1]
        self.castling = components[2]
        self.en_passant = components[3]
        self.fifty_move = int(components[4])
        self.moves = int(components[5])

        board_rows = components[0].split("/")
        assert len(board_rows) == 8

        for i in range(len(board_rows)):
            assert i < 8, f"Got i: {i}"
            row = board_rows[i]
            j = 0
            for char in row:
                if char in set("12345678"):
                    j += (int(char) - 1)  # Prevent double incrementing j
                elif char in set("pnbrqk"):
                    assert j < 8, f"Got (i, j): ({i}, {j}) {row}"
                    self.black_positions[char].set(i, j)
                elif char in set("PNBRQK"):
                    assert j < 8, f"Got (i, j): ({i}, {j})"
                    char = char.lower()
                    self.white_positions[char].set(i, j)
                else:
                    raise ValueError(f"Unexpected piece type encountered: {char}")
                j += 1

    def validate(self) -> None:
        """
        Method to ensure that the board state is valid

        Returns:
            result (int): 1 if valid, 0 otherwise
        """

        # Check for overlapping pieces
        num_pieces = 0
        union_bitboard = BitBoard()

        for k, v in self.black_positions.items():
            union_bitboard += v
            num_pieces += v.get_num_pieces()

        for k, v in self.white_positions.items():
            union_bitboard += v
            num_pieces += v.get_num_pieces()

        assert num_pieces == union_bitboard.get_num_pieces(), f"Overlapping pieces detected: {num_pieces} {union_bitboard.get_num_pieces()}"

    def get_piece(self, row, col) -> str:
        """
        Retrieves piece residing on the specified square

        Args:
            row (int): Specifies the row number
            col (int): Specifies the column number

        Returns:
            piece (str): Single letter representation of the piece
        """

        mask = 1 << 63 - (8 * row + col)

        for piece in self.black_positions:
            if mask & self.black_positions[piece].bitboard:
                return piece

        for piece in self.white_positions:
            if mask & self.white_positions[piece].bitboard:
                return piece.upper()

        return " "

    def show(self) -> None:
        """
        Method to display the current board state
        """

        self.validate()

        print("-" * 17)
        for row_num in range(8):
            for col_num in range(8):
                print("|", end="")
                print(self.get_piece(row_num, col_num), end="")
            print("|")

            print("-" * 17)

        print("BLACK TO MOVE" if self.to_move == -1 else "WHITE TO MOVE")
        print("MOVE NUMBER: " + str(self.moves))

    @property
    def to_move(self) -> int:
        """Get current player move"""
        return self._to_move

    @to_move.setter
    def to_move(self, player: str) -> None:
        if player not in {"w", "b"}:
            raise ValueError(
                "Player value should be either w or b\n" +
                f"Got unexpected value: {player}"
            )
        else:
            self._to_move = -1 if player == "b" else 1

    @property
    def castling(self) -> str:
        return self._castling

    @castling.setter
    def castling(self, state: str) -> None:
        if state not in {
            "----", "---q", "--k-", "--kq",
            "-Q--", "-Q-q", "-Qk-", "-Qkq",
            "K---", "K--q", "K-k-", "K-kq",
            "KQ--", "KQ-q", "KQk-", "KQkq"
        }:
            raise ValueError(f"Invalid castling state: {state}")
        else:
            self._castling = state

    @property
    def en_passant(self) -> str:
        return self._en_passant

    @en_passant.setter
    def en_passant(self, state: str) -> None:
        if(state == "-"):
            self._en_passant = state
        elif len(state) != 2:
            raise ValueError(f"Invalid en passant string length, expected length 2 but got string: {state}")
        elif (state[0] not in set("abcdefgh") or
              state[1] not in set("12345678")):
            raise ValueError(f"Invalid en passant string: {state}")
        else:
            self._en_passant = state

    @property
    def fifty_move(self) -> int:
        return self._fifty_move

    @fifty_move.setter
    def fifty_move(self, num_moves: int) -> None:
        if(not isinstance(num_moves, int) or num_moves < 0):
            raise ValueError(f"Expected non-negative integer for 'fifty_move', instead got: {num_moves}")
        else:
            self._fifty_move = num_moves

    @property
    def moves(self) -> int:
        return self._moves

    @moves.setter
    def moves(self, num_moves: int):
        if(not isinstance(num_moves, int) or num_moves < 1):
            raise ValueError(f"Expected positive integer for 'moves', instead got: {num_moves}")
        else:
            self._moves = num_moves


if __name__ == "__main__":
    board = Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 4")
    board.show()
