from typing import Tuple, Dict

import resources.FENs as FENs
import src.parsers as parsers
from src.bitboard import BitBoard
from src.piece_handler import PieceHandler
from resources.pieces import piece_tokens

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
        self.piece_handler = PieceHandler()

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
            raise ValueError(
                f"Invalid FEN string, expected 6 components instead got {len(components)}"
            )

        # Use custom setter to initialize board_state dictionary
        self.board_state = components

        board_rows = components[0].split("/")
        assert len(board_rows) == 8

        for i, row in enumerate(board_rows):
            assert i < 8, f"Got i: {i}"
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
            for _, black_position in self.black_positions.items():
                bitboard += black_position
        else:
            for _, white_position in self.white_positions.items():
                bitboard += white_position

        return bitboard

    def check_overlap(self) -> None:
        """
        Method to ensure that there is no overlapping pieces

        Returns:
            result (int): 1 if valid, 0 otherwise
        """
        num_pieces = 0
        union_bitboard = BitBoard()

        for _, black_position in self.black_positions.items():
            union_bitboard += black_position
            num_pieces += black_position.count()

        for _, white_position in self.white_positions.items():
            union_bitboard += white_position
            num_pieces += white_position.count()

        assert num_pieces == union_bitboard.count(), \
            f"Overlapping pieces detected: {num_pieces} {union_bitboard.count()}"

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

        for piece, black_position in self.black_positions.items():
            if mask & black_position.bitboard:
                return piece

        for piece, white_position in self.white_positions.items():
            if mask & white_position.bitboard:
                return piece.upper()

        return " "

    def handle_pawn_moves(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
        friendly_pieces: dict,
        opponent_pieces: dict
    ) -> bool:
        """
        Helper method to handle pawn moves, en-passant cases in particular:
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

            # Set the en_passant bitboard
            self.board_state["en_passant"] = BitBoard(
                coordinates=[(end_coord[0] + self.board_state["to_move"], end_coord[1])]
            )
            moved = True
        elif self.board_state["en_passant"].get(*end_coord):
            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces["p"] += end_bitboard

            # Remove captured piece
            capture_bitboard = BitBoard(
                coordinates=[(end_coord[0] + self.board_state["to_move"], end_coord[1])]
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
            if self.board_state["to_move"] == 1 else self.black_positions

        opponent_pieces = self.black_positions \
            if self.board_state["to_move"] == 1 else self.white_positions

        piece_found = False

        for selected_piece in friendly_pieces:
            if friendly_pieces[selected_piece].get(*start_coord):
                piece_found = True
                break

        if not piece_found:
            raise ValueError("ERROR: No friendly piece in selected square")


        legal_moves = self.piece_handler.get_moves(
            self,
            start_coord,
            selected_piece
        )

        if not legal_moves.get(*end_coord):
            raise ValueError(
                f"Illegal move {start_coord}, {end_coord}" + f"\n{str(legal_moves)}"
            )

        pawn_move = False

        if selected_piece == "p":
            pawn_move = self.handle_pawn_moves(
                start_coord,
                end_coord,
                friendly_pieces,
                opponent_pieces
            )

        if not pawn_move:
            # Reset en passant bitboard (if last pawn move was a two square advance)
            self.board_state["en_passant"] = BitBoard()

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
        if self.board_state["to_move"] == -1:  # Updated once every "full" move
            self.board_state["moves"] += 1

        self.board_state["to_move"] = self.board_state["to_move"] * -1


    def __str__(self) -> None:
        self.check_overlap()

        result = ""

        result += ("-" * 17 + "\n")
        for row_num in range(8):
            for col_num in range(8):
                result += "|"
                piece = self.get_piece(row_num, col_num)
                result += piece_tokens[piece]
            result += "|\n"

            result += ("-" * 17 + "\n")

        result += "BLACK TO MOVE\n" if self.board_state["to_move"] == -1 else "WHITE TO MOVE\n"
        result += f"MOVE NUMBER: {self.board_state['moves']}\n"

        return result

    @property
    def board_state(self) -> Dict:
        """Get current board state"""
        return self._board_state

    @board_state.setter
    def board_state(self, components):
        self._board_state = {
            "to_move": self._val_to_move(components[1]),
            "castling": self._val_castling(components[2]),
            "en_passant": self._val_en_passant(components[3]),
            "fifty_move": self._val_fifty_move(components[4]),
            "moves": self._val_moves(components[5])
        }


    def _val_to_move(self, player) -> int:
        if player not in {"w", "b", 1, -1}:
            raise ValueError(
                "Player value should be either w, b, -1 or 1\n" +
                f"Got unexpected value: {player}"
            )
        if player in {"w", "b"}:
            return -1 if player == "b" else 1

        return player


    def _val_castling(self, state: str) -> str:
        if state not in {
            "-", "---q", "--k-", "--kq",
            "-Q--", "-Q-q", "-Qk-", "-Qkq",
            "K---", "K--q", "K-k-", "K-kq",
            "KQ--", "KQ-q", "KQk-", "KQkq"
        }:
            raise ValueError(f"Invalid castling state: {state}")

        return state

    def _val_en_passant(self, state) -> None:
        if isinstance(state, BitBoard):
            return state

        if isinstance(state, str):
            if state == "-":
                return BitBoard()
            if len(state) != 2:
                raise ValueError(f"Invalid en passant string: {state}")
            if (state[0] not in set("abcdefgh") or
                  state[1] not in set("12345678")):
                raise ValueError(f"Invalid en passant string: {state}")

            coords = parsers.alphanumeric_to_index(state)
            return BitBoard(coordinates=[coords])

        raise ValueError(
            f"Invalid en passant input type {type(state)}: {str(state)}"
        )

    def _val_fifty_move(self, num_moves: int) -> None:
        num_moves = int(num_moves)

        if num_moves < 0:
            raise ValueError(
                f"Expected non-negative integer for 'fifty_move', instead got: {num_moves}"
            )

        return num_moves

    def _val_moves(self, num_moves: int):
        num_moves = int(num_moves)

        if num_moves < 1:
            raise ValueError(f"Expected positive integer for 'moves', instead got: {num_moves}")

        return num_moves

