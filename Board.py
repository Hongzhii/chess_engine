import numpy as np
import FENs
import parsers
from bitboard import BitBoard
from pieceHandler import PieceHandler

from typing import Tuple

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


class Board:
    """
    A class to represent any given game state.

    Attributes:
        pieceHandler (PieceHandler): PieceHandler utility class to get moves
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
        fen_string: str = FENs.STARTING_FEN
    ):
        """
        Constructor for the Board class by parsing FEN string

        Args:
            fen_string (str): FEN string representing the board state
        """
        self.pieceHandler = PieceHandler()

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
                    raise ValueError(f"Unexpected piece type: {char}")
                j += 1

    def get_color_bitboard(self, color: int) -> BitBoard:
        """
        Returns bitboard specifying the location of all pieces of a
        specified color

        Args:
            color (int): Specifies color of desired pieces

        Returns:
            bitboard (BitBoard): Bitboard object containing piece
                location information
        """
        bitboard = BitBoard()

        if color == -1:
            for piece in self.black_positions:
                bitboard += self.black_positions[piece]
        else:
            for piece in self.white_positions:
                bitboard += self.white_positions[piece]

        return bitboard

    def check_overlap(self) -> None:
        """
        Method to ensure that there is no overlapping pieces

        Returns:
            result (int): 1 if valid, 0 otherwise
        """
        num_pieces = 0
        union_bitboard = BitBoard()

        for k, v in self.black_positions.items():
            union_bitboard += v
            num_pieces += v.get_num_pieces()

        for k, v in self.white_positions.items():
            union_bitboard += v
            num_pieces += v.get_num_pieces()

        assert num_pieces == union_bitboard.get_num_pieces(), f"Overlapping pieces detected: {num_pieces} {union_bitboard.get_num_pieces()}"

    def get_piece(self, row: int, col: int) -> str:
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

    def handle_enpassant(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
        friendly_pieces: dict,
        opponent_pieces: dict
    ) -> bool:
        """
        Helper method to handle en-passant cases:
            1. Set en_passant bitboard for two square advances
            2. Remove the correct opponent piece for en-passant captures

        Args:
            start_coord (Tuple): Piece start coordinates
            end_coord (Tuple): Piece end coordinates
            friendly_pieces (dict): Locations of friendly pieces
            opponent_pieces (dict): Locations of opponent pieces

        Returns:
            moved (bool): Represents whether or not pawn move was handled by
                en passant helper method
        """
        moved = False

        start_bitboard = BitBoard(coordinates=[start_coord])
        end_bitboard = BitBoard(coordinates=[end_coord])

        if abs(start_coord[0] - end_coord[0]) == 2:
            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces["p"] += end_bitboard
            moved = True
        elif self.en_passant.get(*end_coord):
            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces["p"] += end_bitboard

            # Remove captured piece
            capture_bitboard = BitBoard(
                coordinates=[(end_coord[0] + self.to_move, end_coord[1])]
            )
            opponent_pieces["p"] -= capture_bitboard
            moved = True
        return moved

    def move(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int]
    ) -> None:
        """
        Verifies and executes move on the board

        Args:
            start_coords (Tuple): Tuple specifying start coordinates
            end_coords (Tuple): Tuple specifying end coordinates
        """
        friendly_pieces = self.white_positions \
            if self.to_move == 1 else self.black_positions

        opponent_pieces = self.black_positions \
            if self.to_move == 1 else self.white_positions

        for selected_piece in friendly_pieces:
            if friendly_pieces[selected_piece].get(*start_coord):
                break

        legal_moves = self.pieceHandler.get_moves(
            self,
            start_coord,
            selected_piece
        )

        if not legal_moves.get(*end_coord):
            raise ValueError(f"Illegal move {start_coord}, {end_coord}" + f"{legal_moves.show()}")

        en_passant_move = False

        if selected_piece == "p":
            en_passant_move = self.handle_enpassant(
                start_coord,
                end_coord,
                friendly_pieces,
                opponent_pieces
            )

        if not en_passant_move:
            start_bitboard = BitBoard(coordinates=[start_coord])
            end_bitboard = BitBoard(coordinates=[end_coord])

            # Update friendly piece
            piece_bitboard = friendly_pieces[selected_piece]
            friendly_pieces[selected_piece] = piece_bitboard ^ start_bitboard
            friendly_pieces[selected_piece] += end_bitboard

            # Update opponent piece (if any)
            for piece in opponent_pieces:
                opponent_pieces[piece] -= end_bitboard

        # Update other attributes
        self.to_move = self.to_move * -1

        if self.to_move == 1:  # Updated once every "full" move
            self.moves += 1

    def show(self) -> None:
        """
        Method to display the current board state
        """

        self.check_overlap()

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
    def to_move(self, player) -> None:
        if player not in {"w", "b", 1, -1}:
            raise ValueError(
                "Player value should be either w, b, -1 or 1\n" +
                f"Got unexpected value: {player}"
            )
        elif player in {"w", "b"}:
            self._to_move = -1 if player == "b" else 1
        else:
            self._to_move = player

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
    def en_passant(self) -> BitBoard:
        return self._en_passant

    @en_passant.setter
    def en_passant(self, state) -> None:
        if isinstance(state, BitBoard):
            self._en_passant = state
        elif isinstance(state, str):
            if(state == "-"):
                self._en_passant = BitBoard()
            elif len(state) != 2:
                raise ValueError(f"Invalid en passant string: {state}")
            elif (state[0] not in set("abcdefgh") or
                  state[1] not in set("12345678")):
                raise ValueError(f"Invalid en passant string: {state}")
            else:
                coords = parsers.alphanumeric_to_index(state)
                self._en_passant = BitBoard(coordinates=[coords])

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
    board = Board(FENs.FOURKNIGHTS_FEN)
    board.show()
