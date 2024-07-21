import parsers
import FENs
from board import Board
from bitboard import BitBoard
from typing import Tuple

WHITE_PIECES = set("PNBRQK")
BLACK_PIECES = set("pnbrqk")


class PieceHandler:
    """
    A utility class to retrieve legal moves for a given piece on a board
    """
    @staticmethod
    def _in_range(
        row: int,
        col: int
    ) -> bool:
        """
        Helper function to check if a given position is inside of a chessboard

        Args:
        row (int): Row index of piece
        col(int): Column index of piece

        Returns:
        isValid (bool): Whether or not position is within chessboard
        """
        i_valid = 0 <= row and row <= 7
        j_valid = 0 <= col and col <= 7

        return i_valid and j_valid

    @classmethod
    def _get_pawn_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) == 'p'
        else:
            assert board.get_piece(position[0], position[1]) == 'P'

        bitboard = BitBoard()

        all_pieces = board.get_color_bitboard(1) + board.get_color_bitboard(-1)

        if color == -1:
            if not all_pieces.get(position[0] + 1, position[1]):
                bitboard.set(position[0] + 1, position[1])
            
            if position[0] == 1 and \
                    not all_pieces.get(position[0] + 2, position[1]):
                bitboard.set(position[0] + 2, position[1])
        else:
            if not all_pieces.get(position[0] - 1, position[1]):
                bitboard.set(position[0] - 1, position[1])
            
            if position[0] == 1 and \
                    not all_pieces.get(position[0] - 2, position[1]):
                bitboard.set(position[0] - 2, position[1])

        # List possible captures
        if color == -1:
            candidate_locations = [
                (position[0] + 1, position[1] + 1),
                (position[0] + 1, position[1] - 1)
            ]
        else:
            candidate_locations = [
                (position[0] - 1, position[1] + 1),
                (position[0] - 1, position[1] - 1)
            ]

        capture_bitboard = BitBoard()

        for location in candidate_locations:
            if cls._in_range(location[0], location[1]):
                capture_bitboard.set(location[0], location[1])

        opp_bitboard = board.get_color_bitboard(color * -1)

        # Handle en-passant
        ep_position = parsers.alphanumeric_to_index(board.en_passant)
        if ep_position is not None:
            opp_bitboard.set(ep_position[0], ep_position[1])

        capture_bitboard = capture_bitboard & opp_bitboard

        bitboard += capture_bitboard

        return bitboard

    @classmethod
    def _get_knight_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) == 'n'
        else:
            assert board.get_piece(position[0], position[1]) == 'N'

        bitboard = BitBoard()

        candidate_locations = [
            (position[0] + 2, position[1] + 1),
            (position[0] + 2, position[1] - 1),
            (position[0] - 2, position[1] + 1),
            (position[0] - 2, position[1] - 1),
            (position[0] + 1, position[1] + 2),
            (position[0] - 1, position[1] + 2),
            (position[0] + 1, position[1] - 2),
            (position[0] - 1, position[1] - 2)
        ]

        for location in candidate_locations:
            if cls._in_range(location[0], location[1]):
                bitboard.set(location[0], location[1])

        # Check if knight is attacking friendly pieces
        friendly_bitboard = board.get_color_bitboard(color)
        friendly_bitboard = friendly_bitboard & bitboard

        bitboard = bitboard ^ friendly_bitboard

        return bitboard

    @classmethod
    def _get_bishop_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) in set("bq")
        else:
            assert board.get_piece(position[0], position[1]) in set("BQ")

        bitboard = BitBoard()

        friendly_bitboard = board.get_color_bitboard(color)
        opponent_bitboard = board.get_color_bitboard(color * -1)

        for i in [-1, 1]:
            for j in [-1, 1]:
                row_index = position[0]
                col_index = position[1]
                while True:
                    row_index += i
                    col_index += j

                    if not cls._in_range(row_index, col_index):
                        break
                    elif friendly_bitboard.get(row_index, col_index):
                        break

                    bitboard.set(row_index, col_index)

                    if opponent_bitboard.get(row_index, col_index):
                        break

        return bitboard

    @classmethod
    def _get_rook_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) in set("rq")
        else:
            assert board.get_piece(position[0], position[1]) in set("RQ")

        bitboard = BitBoard()

        friendly_bitboard = board.get_color_bitboard(color)
        opponent_bitboard = board.get_color_bitboard(color * -1)

        for i in [-1, 1]:
            index = position[0]
            while True:
                index += i

                if not cls._in_range(index, position[1]):
                    break
                elif friendly_bitboard.get(index, position[1]):
                    break

                bitboard.set(index, position[1])

                if opponent_bitboard.get(index, position[1]):
                    break

            index = position[1]
            while True:
                index += i

                if not cls._in_range(position[0], index):
                    break
                elif friendly_bitboard.get(position[0], index):
                    break

                bitboard.set(position[0], index)

                if opponent_bitboard.get(position[0], index):
                    break

        return bitboard

    @classmethod
    def _get_queen_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) == 'q'
        else:
            assert board.get_piece(position[0], position[1]) == 'Q'

        bishop_component = cls._get_bishop_moves(board, color, position)
        rook_component = cls._get_rook_moves(board, color, position)

        return bishop_component + rook_component

    @classmethod
    def _get_king_moves(
        cls,
        board: Board,
        color: int,
        position: Tuple[int, int]
    ) -> BitBoard:
        if color == -1:
            assert board.get_piece(position[0], position[1]) == 'k'
        else:
            assert board.get_piece(position[0], position[1]) == 'K'

        bitboard = BitBoard()

        candidate_locations = [
            (position[0] + 1, position[1]),
            (position[0] - 1, position[1]),
            (position[0], position[1] + 1),
            (position[0], position[1] - 1),
            (position[0] + 1, position[1] + 1),
            (position[0] + 1, position[1] - 1),
            (position[0] - 1, position[1] + 1),
            (position[0] - 1, position[1] - 1),
        ]

        friendly_bitboard = board.get_color_bitboard(color)

        for location in candidate_locations:
            if cls._in_range(location[0], location[1]) \
                    and not friendly_bitboard.get(location[0], location[1]):
                bitboard.set(location[0], location[1])

        return bitboard

    @classmethod
    def get_moves(
        cls,
        board: Board,
        position: Tuple[int, int],
        piece_type: str
    ) -> BitBoard:
        """
        Returns a bitboard of moves taking into account captures and
        friendly pieces

        Args:
            board (Board): Board state information
            position (Tuple[int, int]): Position of piece being moved
            piece_type (str): Piece being moved
        """
        assert piece_type in set("pnbrqkPNBRQK")

        color = -1 if piece_type in set("pnbrqk") else 1

        if piece_type.lower() == "p":
            return cls._get_pawn_moves(board, color, position)
        elif piece_type.lower() == "n":
            return cls._get_knight_moves(board, color, position)
        elif piece_type.lower() == "b":
            return cls._get_bishop_moves(board, color, position)
        elif piece_type.lower() == "r":
            return cls._get_rook_moves(board, color, position)
        elif piece_type.lower() == "q":
            return cls._get_queen_moves(board, color, position)
        else:
            return cls._get_king_moves(board, color, position)


if __name__ == "__main__":
    handler = PieceHandler()
    print("======EN PASSANT TEST CASE======")
    board = Board(FENs.ENPASSANT_FEN)
    board.show()
    
    print("Pawn Moves:")
    print("(En-passant pawn)")
    handler.get_moves(board, (3, 4), "P").show()

    print("======FOUR KNIGHTS TESTCASE======")
    board = Board(FENs.FOURKNIGHTS_FEN)
    board.show()
    print("Knight Moves:")
    handler.get_moves(board, (5, 5), "N").show()
    handler.get_moves(board, (5, 2), "N").show()
    handler.get_moves(board, (2, 5), "n").show()
    handler.get_moves(board, (2, 2), "n").show()

    print("Bishop Moves:")
    handler.get_moves(board, (7, 5), "B").show()
    handler.get_moves(board, (7, 2), "B").show()
    handler.get_moves(board, (0, 5), "b").show()
    handler.get_moves(board, (0, 2), "b").show()

    print("Queen Moves:")
    handler.get_moves(board, (7, 3), "Q").show()
    handler.get_moves(board, (0, 3), "q").show()

    print("King Moves:")
    handler.get_moves(board, (7, 4), "K").show()
    handler.get_moves(board, (0, 4), "k").show()
