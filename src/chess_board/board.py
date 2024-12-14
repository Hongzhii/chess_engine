import copy

from typing import Tuple, Dict, List

from resources import FENs, hash_keys
from resources.pieces import piece_tokens

from src.chess_board import parsers
from src.chess_board.bitboard import BitBoard
from src.chess_board import piece_handler

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
        fen_string: str = FENs.STARTING_FEN
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

    def in_check(
        self,
        return_target_bitboard: bool = False,
    ) -> bool | BitBoard:
        """
        Method to determine if current player is in check

        Args:
            return_target_bitboard (bool): If set to True, function returns the target bitboard
                instead of a bool value. This is useful for preventing castling through check

        Returns:
            bool_result (bool): True if in check, False otherwise
            bitboard_result (BitBoard): BitBoard containing the locations being targeted by
                opponent pieces
        """
        to_move = self.board_state["to_move"]
        self.board_state["to_move"] *= -1  # Change to opponents move for piece targeting

        if to_move == 1:
            king_bitboard = self.white_positions["k"]
            opponent_positions = self.black_positions
        else:
            king_bitboard = self.black_positions["k"]
            opponent_positions = self.white_positions

        target_bitboard = BitBoard()

        # Handle pawn moves separately, pawn movement action does not imply the ability to capture
        pawn_bitboard = BitBoard()
        pawn_positions = opponent_positions["p"].get_coordinates()

        for position in pawn_positions:
            pawn_bitboard += piece_handler.get_pawn_moves(
                board=self,
                position=position,
                captures_only=True,
            )

        target_bitboard += pawn_bitboard

        # Process remaining pieces
        target_move_functions = [
            (piece_handler.get_knight_moves, "n"),
            (piece_handler.get_bishop_moves, "b"),
            (piece_handler.get_rook_moves, "r"),
            (piece_handler.get_queen_moves, "q"),
        ]

        for func, piece_type in target_move_functions:
            piece_bitboard = BitBoard()
            piece_positions = opponent_positions[piece_type].get_coordinates()

            for position in piece_positions:
                piece_bitboard += func(
                    board=self,
                    position=position,
                )

            target_bitboard += piece_bitboard

        # Reset to_move to original state
        self.board_state["to_move"] *= -1

        if return_target_bitboard:
            return target_bitboard

        return (target_bitboard - king_bitboard) != target_bitboard

    def handle_king_moves(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
    ) -> bool:
        """
        Helper method to handle king moves, castling cases in particular.

        Args:
            start_coord (Tuple): Piece start coordinates
            end_coord (Tuple): Piece end coordinates

        Returns:
            None
        """
        friendly_pieces = self.white_positions \
            if self.board_state["to_move"] == 1 else self.black_positions

        opponent_pieces = self.black_positions \
            if self.board_state["to_move"] == 1 else self.white_positions

        start_bitboard = BitBoard(coordinates=[start_coord])
        end_bitboard = BitBoard(coordinates=[end_coord])

        if start_coord[1] - end_coord[1] == 2:  # Queenside castling
            friendly_pieces["k"] -= start_bitboard
            friendly_pieces["k"] += end_bitboard

            rook_start_bitboard = BitBoard(coordinates=[(start_coord[0], 0)])
            rook_end_bitboard = BitBoard(coordinates=[(start_coord[0], 3)])

            friendly_pieces["r"] -= rook_start_bitboard
            friendly_pieces["r"] += rook_end_bitboard

        elif start_coord[1] - end_coord[1] == -2: # Kingside castling
            friendly_pieces["k"] -= start_bitboard
            friendly_pieces["k"] += end_bitboard

            rook_start_bitboard = BitBoard(coordinates=[(start_coord[0], 7)])
            rook_end_bitboard = BitBoard(coordinates=[(start_coord[0], 5)])

            friendly_pieces["r"] -= rook_start_bitboard
            friendly_pieces["r"] += rook_end_bitboard

        else:
            # Update friendly pieces
            friendly_pieces["k"] -= start_bitboard
            friendly_pieces["k"] += end_bitboard

            # Remove captured pieces
            for piece in opponent_pieces:
                opponent_pieces[piece] -= end_bitboard

        # Any king move (non-castling moves included) forfeits the right to castle in the future
        if self.board_state["castling"] == "-":
            return

        if self.board_state["to_move"] == 1:
            self.board_state["castling"] = "--" + self.board_state["castling"][2:]
        else:
            self.board_state["castling"] = self.board_state["castling"][:2] + "--"

        if self.board_state["castling"] == "----":
            self.board_state["castling"] = "-"

    def handle_pawn_moves(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
        promotion_piece_type: str,
    ) -> None:
        """
        Helper method to handle pawn moves, en-passant cases in particular.
            1. Set en_passant bitboard for two square advances
            2. Remove the correct opponent piece for en-passant captures

        Args:
            start_coord (Tuple): Piece start coordinates
            end_coord (Tuple): Piece end coordinates

        Returns:
            None
        """
        friendly_pieces = self.white_positions \
            if self.board_state["to_move"] == 1 else self.black_positions

        opponent_pieces = self.black_positions \
            if self.board_state["to_move"] == 1 else self.white_positions

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
        elif self.board_state["en_passant"].is_occupied(*end_coord):
            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces["p"] += end_bitboard

            # Remove captured piece
            capture_bitboard = BitBoard(
                coordinates=[(end_coord[0] + self.board_state["to_move"], end_coord[1])]
            )
            opponent_pieces["p"] -= capture_bitboard
        elif end_coord[0] == 0 or end_coord[0] == 7:  # Promotions
            if promotion_piece_type is None:
                raise ValueError("Need to specify piece type for promotion move: n, b, r or q")

            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces[promotion_piece_type] += end_bitboard

            # Remove captured pieces
            for piece in opponent_pieces:
                opponent_pieces[piece] -= end_bitboard
        else:
            # Update friendly pieces
            friendly_pieces["p"] -= start_bitboard
            friendly_pieces["p"] += end_bitboard

            # Remove captured pieces
            for piece in opponent_pieces:
                opponent_pieces[piece] -= end_bitboard
    
    def check_rook_positions(
        self,
    ) -> None:
        """
        Helper method to check rook status and update castling board state accordingly.

        Args:
            None
        
        Returns:
            None
        """
        if self.board_state["castling"] == "-":
            return
        
        castling_state = self.board_state["castling"]
        
        if not self.white_positions["r"].is_occupied(7, 7):
            castling_state = "".join([
                "-",
                castling_state[1],
                castling_state[2],
                castling_state[3],
            ])
        if not self.white_positions["r"].is_occupied(7, 0):
            castling_state = "".join([
                castling_state[0],
                "-",
                castling_state[2],
                castling_state[3],
            ])
        if not self.black_positions["r"].is_occupied(0, 7):
            castling_state = "".join([
                castling_state[0],
                castling_state[1],
                "-",
                castling_state[3],
            ])
        if not self.black_positions["r"].is_occupied(0, 0):
            castling_state = "".join([
                castling_state[0],
                castling_state[1],
                castling_state[2],
                "-",
            ])

        if castling_state == "----":
            castling_state = "-"
        
        self.board_state["castling"] = castling_state

    def move(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
        promotion_piece_type: str = None,
    ) -> None:
        """
        Verifies and executes move on the board

        Args:
            start_coords (Tuple): Tuple specifying start coordinates
            end_coords (Tuple): Tuple specifying end coordinates
            promotion_piece_type (str): String specifying which piece to promote to, if applicable

        Returns:
            None
        """
        friendly_pieces = self.white_positions \
            if self.board_state["to_move"] == 1 else self.black_positions

        opponent_pieces = self.black_positions \
            if self.board_state["to_move"] == 1 else self.white_positions

        piece_found = False

        for selected_piece, piece_bitboard in friendly_pieces.items():
            if piece_bitboard.is_occupied(*start_coord):
                piece_found = True
                break

        if not piece_found:
            raise ValueError("ERROR: No friendly piece in selected square")


        legal_moves = piece_handler.get_moves(
            self,
            start_coord,
            selected_piece
        )

        if not legal_moves.is_occupied(*end_coord):
            raise ValueError(
                f"Illegal move {start_coord}, {end_coord}" + f"\n{str(legal_moves)}"
            )

        # Pawn and king moves need to be handled separately to deal with castling and en passant.
        # These moves require two pieces on different squares to be updated concurrently
        if selected_piece == "p":
            self.handle_pawn_moves(
                start_coord,
                end_coord,
                promotion_piece_type,
            )
        elif selected_piece == "k":
            self.handle_king_moves(
                start_coord,
                end_coord,
            )
        else:
            start_bitboard = BitBoard(coordinates=[start_coord])
            end_bitboard = BitBoard(coordinates=[end_coord])

            # Update friendly piece
            piece_bitboard = friendly_pieces[selected_piece]
            friendly_pieces[selected_piece] = piece_bitboard ^ start_bitboard
            friendly_pieces[selected_piece] += end_bitboard

            # Update opponent piece (if any)
            for piece in opponent_pieces:
                opponent_pieces[piece] -= end_bitboard

        self.check_rook_positions()

        if selected_piece != "p":
            # Reset en passant bitboard (if last pawn move was a two square advance)
            self.board_state["en_passant"] = BitBoard()

        if self.board_state["to_move"] == -1:  # Updated once every "full" move
            self.board_state["moves"] += 1

        self.board_state["to_move"] = self.board_state["to_move"] * -1

        self.check_overlap()

    def check_move(
        self,
        start_coord: Tuple[int, int],
        end_coord: Tuple[int, int],
        promotion_piece_type: str = None,
    ) -> bool:
        """
        Returns True if a move is legal, False otherwise

        Args:
            start_coords (Tuple): Tuple specifying start coordinates
            end_coords (Tuple): Tuple specifying end coordinates
            promotion_piece_type (str): String specifying which piece to promote to, if applicable

        Returns:
            result (bool): Boolean value specifying whether or not move is legal
        """
        # Create a new copy of the board to execute the move on
        temp_board = copy.deepcopy(self)

        # Execute_move
        temp_board.move(
            start_coord,
            end_coord,
            promotion_piece_type,
        )
        temp_board.board_state["to_move"] = self.board_state["to_move"]

        return not temp_board.in_check()

    def get_legal_moves(
        self
    ) -> List[Tuple[Tuple, Tuple, str]]:
        """
        Returns a list of legal moves on the given board in the form of a tuple.

        Returns:
            legal_moves: Tuple in the form -> (<start_coord>, <end_coord>, <promotion_piece_type>)
        """

        pseudo_legal_moves = []

        friendly_pieces = self.white_positions if self.board_state["to_move"] == 1 \
            else self.black_positions

        for piece, piece_bitboard in friendly_pieces.items():
            piece_coordinates = piece_bitboard.get_coordinates()

            for coord in piece_coordinates:
                end_coords = piece_handler.get_moves(
                    board=self,
                    position=coord,
                    piece_type=piece,
                ).get_coordinates()

                pseudo_legal_moves += zip(
                    [coord] * len(end_coords),
                    end_coords,
                    [None] * len(end_coords),
                )
        
        for i, move in enumerate(pseudo_legal_moves):
            if (move[1][0] == 0 or move[1][0] == 7) and move[2] is not None:
                promotion_move = pseudo_legal_moves.pop(i)

                all_promotions = [
                    (promotion_move[0], promotion_move[1], "b"),
                    (promotion_move[0], promotion_move[1], "n"),
                    (promotion_move[0], promotion_move[1], "r"),
                    (promotion_move[0], promotion_move[1], "q"),
                ]

                pseudo_legal_moves += all_promotions

        return [move for move in pseudo_legal_moves if self.check_move(*move)]
    
    def hash(self):
        """
        Returns the hash value of the current position using Zobrist hash keys specified in the
        resources directory.

        Returns:
            hash (int): Hashed value of the board position
        """
        hash = 0
        hash_key_dict = hash_keys.HASH_KEYS

        # Process white piece positions
        for piece, piece_bitboard in self.white_positions.items():
            for coord in piece_bitboard.get_coordinates():
                coord_key = f"{coord[0]}{coord[1]}"
                hash = hash ^ hash_key_dict["position"][coord_key][piece]

        # Process black piece positions
        for piece, piece_bitboard in self.black_positions.items():
            for coord in piece_bitboard.get_coordinates():
                coord_key = f"{coord[0]}{coord[1]}"
                hash = hash ^ hash_key_dict["position"][coord_key][piece]

        # Process castling state
        hash = hash ^ hash_key_dict["castling"][self.board_state["castling"]]

        # Process en passant
        en_passant_square = self.board_state["en_passant"].get_coordinates()

        if len(en_passant_square) == 1:
            hash = hash ^ hash_key_dict["en_passant"][en_passant_square[0][1]]

        # Process to_move state
        if self.board_state["to_move"] == 1:
            hash = hash ^ hash_key_dict["to_move"]

        return hash

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
