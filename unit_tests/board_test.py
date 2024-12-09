import unittest

from src.board import Board
from resources.FENs import (
    STARTING_FEN,
    FOURKNIGHTS_FEN,
    LONDON_FEN,
    CASTLING_FEN,
    ILLEGAL_CASTLING_THROUGH_CHECK_1_FEN,
    ILLEGAL_CASTLING_THROUGH_CHECK_2_FEN,
    ILLEGAL_CASTLING_BLACK_IN_CHECK,
    ILLEGAL_CASTLING_WHITE_IN_CHECK,
)
from resources.starting_position_string import STARTING_POSITION_STRING_OUTPUT

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

        # Hardcode the starting position
        STARTING_WHITE = {
            "p": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "11111111",
                "00000000",
            ]), 2),
            "n": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "01000010",
            ]), 2),
            "b": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
            ]), 2),
            "r": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000001",
            ]), 2),
            "q": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
            ]), 2),
        }
        STARTING_BLACK= {
            "p": int("".join([
                "00000000",
                "11111111",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n": int("".join([
                "01000010",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b": int("".join([
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r": int("".join([
                "10000001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q": int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k": int("".join([
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        for k in self.board.white_positions:
            self.board.white_positions[k].bitboard = STARTING_WHITE[k]

        for k in self.board.black_positions:
            self.board.black_positions[k].bitboard = STARTING_BLACK[k]


    # Test FEN constructor
    def test_constructor(self):
        EXPECTED_LONDON_WHITE = {
            "p": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
                "00101000",
                "11000111",
                "00000000",
            ]), 2),
            "n": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000100",
                "00010000",
                "00000000",
            ]), 2),
            "b": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000100",
                "00010000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000100",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000010",
            ]), 2),
        }
        EXPECTED_LONDON_BLACK = {
            "p":int("".join([
                "00000000",
                "11000111",
                "00001000",
                "00110000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00001000",
                "00000000",
                "00000100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "10000100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00000010",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }
        EXPECTED_4KNIGHTS_WHITE = {
            "p":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "00000000",
                "11110111",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000001",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
            ]), 2),
        }
        EXPECTED_4KNIGHTS_BLACK = {
            "p":int("".join([
                "00000000",
                "11110111",
                "00000000",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":
            int("".join([
                "00000000",
                "00000000",
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "10000001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        london = Board(LONDON_FEN)

        for k, v in london.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_LONDON_WHITE[k])

        for k, v in london.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_LONDON_BLACK[k])

        four_knights = Board(FOURKNIGHTS_FEN)

        for k, v in four_knights.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_4KNIGHTS_WHITE[k])

        for k, v in four_knights.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_4KNIGHTS_BLACK[k])

        starting = Board(STARTING_FEN)

        for k, v in starting.white_positions.items():
            self.assertEqual(v.bitboard, self.board.white_positions[k].bitboard)

        for k, v in starting.black_positions.items():
            self.assertEqual(v.bitboard, self.board.black_positions[k].bitboard)


    # Test overlap detection
    def test_overlap_detection(self):
        # Create overlapping pieces
        self.board.black_positions["p"].bitboard = int("".join([
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
        ]), 2)

        with self.assertRaises(AssertionError):
            self.board.check_overlap()

        self.board.black_positions["p"].bitboard = int("".join([
            "11111111",
            "11111111",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)

        with self.assertRaises(AssertionError):
            self.board.check_overlap()

        self.board.black_positions["p"].bitboard = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "11111111",
            "11111111",
        ]), 2)

        with self.assertRaises(AssertionError):
            self.board.check_overlap()

        # Board should not overlap
        self.board.black_positions["p"].bitboard = int("".join([
            "00000000",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "11111111",
            "00000000",
            "00000000",
        ]), 2)

        self.board.check_overlap()

    # Test in-check detection method
    def test_in_check(self):
        """
        This test case tests the functionality of the in_check() method.

        Other involved methods/functionalities:
            piece_handler.py
                _get_{piece}_moves.py
        """
        with self.subTest():
            board = Board(ILLEGAL_CASTLING_WHITE_IN_CHECK)
            self.assertTrue(board.in_check())

        with self.subTest():
            board = Board(ILLEGAL_CASTLING_BLACK_IN_CHECK)
            self.assertTrue(board.in_check())

        with self.subTest():
            board = Board()
            self.assertFalse(board.in_check())

        with self.subTest():
            board = Board()
            board.move((6, 4), (4, 4))
            self.assertFalse(board.in_check())

        with self.subTest():
            board = Board()
            self.assertFalse(board.in_check())
            self.assertEqual(board.board_state["to_move"], 1)
            self.assertFalse(board.in_check())
            self.assertEqual(board.board_state["to_move"], 1)

# ============================== START TEST move() ==============================
    """
    The following are a set of high level tests for verifying the functionality of
    the move() method.

    Other involved methods/functionalities:
        board.py
            __init__() FEN constructor
            handle_pawn_moves()
            handle_king_moves()
            `to_move` and `moves` board state attributes
        piece_handler.py
            get_moves()
        bitboard.py
            get()
    """

    def test_move_regular(self):
        EXPECTED_WHITE_POSITION = {
            "p":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "00000000",
                "11110111",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000001",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
            ]), 2),
        }
        EXPECTED_BLACK_POSITION = {
            "p":int("".join([
                "00000000",
                "11110111",
                "00000000",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":
            int("".join([
                "00000000",
                "00000000",
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "10000001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 1)

        self.board.move(start_coord=(6, 4), end_coord=(4, 4))

        self.assertEqual(self.board.board_state["to_move"], -1)
        self.assertEqual(self.board.board_state["moves"], 1)

        self.board.move(start_coord=(1, 4), end_coord=(3, 4))
        self.board.move(start_coord=(7, 6), end_coord=(5, 5))
        self.board.move(start_coord=(0, 6), end_coord=(2, 5))
        self.board.move(start_coord=(7, 1), end_coord=(5, 2))
        self.board.move(start_coord=(0, 1), end_coord=(2, 2))

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 4)

        for k, v in self.board.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_WHITE_POSITION[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_BLACK_POSITION[k])

    def test_move_captures(self):
        EXPECTED_WHITE_POSITION = {
            "p": int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "11100111",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "00000000",
                "00000000",
                "00000010",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000001",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
            ]), 2),
        }
        EXPECTED_BLACK_POSITION = {
            "p":int("".join([
                "00000000",
                "11100111",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000010",
                "00000000",
                "00000000",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "10000001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        self.board.move(start_coord=(6, 4), end_coord=(4, 4))
        self.board.move(start_coord=(1, 4), end_coord=(3, 4))
        self.board.move(start_coord=(6, 3), end_coord=(4, 3))
        self.board.move(start_coord=(1, 3), end_coord=(3, 3))
        self.board.move(start_coord=(7, 1), end_coord=(5, 2))
        self.board.move(start_coord=(0, 1), end_coord=(2, 2))
        self.board.move(start_coord=(4, 3), end_coord=(3, 4))
        self.board.move(start_coord=(3, 3), end_coord=(4, 4))
        self.board.move(start_coord=(5, 2), end_coord=(4, 4))
        self.board.move(start_coord=(2, 2), end_coord=(3, 4))

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 6)

        for k, v in self.board.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_WHITE_POSITION[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_BLACK_POSITION[k])

    def test_move_en_passant(self):
        EXPECTED_WHITE_POSITION = {
            "p":int("".join([
                "00000000",
                "00000000",
                "01000000",
                "00000000",
                "00000000",
                "00000000",
                "01111111",
                "00000000",
            ]),2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "01000010",
            ]),2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100100",
            ]),2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000001",
            ]),2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]),2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
            ]),2),
        }
        EXPECTED_BLACK_POSITION = {
            "p":int("".join([
                "00000000",
                "00111111",
                "10000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
            "n":int("".join([
                "01000010",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
            "b":int("".join([
                "00100100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
            "r":int("".join([
                "10000001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
            "k":int("".join([
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]),2),
        }

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 1)

        self.board.move(start_coord=(6, 0), end_coord=(4, 0))
        self.board.move(start_coord=(1, 0), end_coord=(2, 0))
        self.board.move(start_coord=(4, 0), end_coord=(3, 0))
        self.board.move(start_coord=(1, 1), end_coord=(3, 1))
        self.board.move(start_coord=(3, 0), end_coord=(2, 1))

        self.assertEqual(self.board.board_state["to_move"], -1)
        self.assertEqual(self.board.board_state["moves"], 3)

        for k, v in self.board.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_WHITE_POSITION[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_BLACK_POSITION[k])


    def test_move_kingside_castling(self):
        EXPECTED_WHITE_POSITION = {
            "p":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "11110111",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000100",
                "00000000",
                "01000000",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "00100000",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "10000100",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000010",
            ]), 2),
        }
        EXPECTED_BLACK_POSITION = {
            "p":int("".join([
                "00000000",
                "11110111",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":int("".join([
                "01000000",
                "00000000",
                "00000100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00100000",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":
            int("".join([
                "10000100",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00000010",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 1)

        self.board.move(start_coord=(6, 4), end_coord=(5, 4))
        self.board.move(start_coord=(1, 4), end_coord=(2, 4))
        self.board.move(start_coord=(7, 6), end_coord=(5, 5))
        self.board.move(start_coord=(0, 6), end_coord=(2, 5))
        self.board.move(start_coord=(7, 5), end_coord=(6, 4))
        self.board.move(start_coord=(0, 5), end_coord=(1, 4))
        self.board.move(start_coord=(7, 4), end_coord=(7, 6))
        self.board.move(start_coord=(0, 4), end_coord=(0, 6))

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 5)

        for k, v in self.board.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_WHITE_POSITION[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_BLACK_POSITION[k])


    def test_move_queenside_castling(self):
        EXPECTED_WHITE_POSITION = {
            "p":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
                "11101111",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100000",
                "00000000",
                "00000010",
            ]), 2),
            "b":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00001000",
                "00000000",
                "00000100",
            ]), 2),
            "r":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010001",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00010000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00100000",
            ]), 2),
        }
        EXPECTED_BLACK_POSITION = {
            "p":int("".join([
                "00000000",
                "11101111",
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "n":int("".join([
                "00000010",
                "00000000",
                "00100000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "b":int("".join([
                "00000100",
                "00000000",
                "00001000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "r":int("".join([
                "00010001",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "q":int("".join([
                "00000000",
                "00010000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
            "k":int("".join([
                "00100000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
                "00000000",
            ]), 2),
        }

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 1)

        self.board.move(start_coord=(6, 3), end_coord=(5, 3))
        self.board.move(start_coord=(1, 3), end_coord=(2, 3))
        self.board.move(start_coord=(7, 1), end_coord=(5, 2))
        self.board.move(start_coord=(0, 1), end_coord=(2, 2))
        self.board.move(start_coord=(7, 2), end_coord=(5, 4))
        self.board.move(start_coord=(0, 2), end_coord=(2, 4))
        self.board.move(start_coord=(7, 3), end_coord=(6, 3))
        self.board.move(start_coord=(0, 3), end_coord=(1, 3))
        self.board.move(start_coord=(7, 4), end_coord=(7, 2))
        self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        self.assertEqual(self.board.board_state["to_move"], 1)
        self.assertEqual(self.board.board_state["moves"], 6)

        for k, v in self.board.white_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_WHITE_POSITION[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_BLACK_POSITION[k])


    def test_move_rook_castling_kingside_forfeit(self):
        self.board = Board(CASTLING_FEN)
        self.board.move(start_coord=(7, 7), end_coord=(7, 6))
        self.assertEqual(self.board.board_state["castling"], "-Qkq")

        self.board.move(start_coord=(0, 7), end_coord=(0, 6))
        self.assertEqual(self.board.board_state["castling"], "-Q-q")

        self.board.move(start_coord=(7, 6), end_coord=(7, 7))
        self.board.move(start_coord=(0, 6), end_coord=(0, 7))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 6))

        self.board.move(start_coord=(7, 4), end_coord=(7, 2))
        self.assertEqual(self.board.board_state["castling"], "---q")

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 6))

        self.board.move(start_coord=(0, 4), end_coord=(0, 2))
        self.assertEqual(self.board.board_state["castling"], "-")

    def test_move_rook_castling_queenside_forfeit(self):
        self.board = Board(CASTLING_FEN)

        self.board.move(start_coord=(7, 0), end_coord=(7, 1))
        self.assertEqual(self.board.board_state["castling"], "K-kq")

        self.board.move(start_coord=(0, 0), end_coord=(0, 1))
        self.assertEqual(self.board.board_state["castling"], "K-k-")

        self.board.move(start_coord=(7, 1), end_coord=(7, 0))
        self.board.move(start_coord=(0, 1), end_coord=(0, 0))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 2))

        self.board.move(start_coord=(7, 4), end_coord=(7, 6))
        self.assertEqual(self.board.board_state["castling"], "--k-")

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        self.board.move(start_coord=(0, 4), end_coord=(0, 6))
        self.assertEqual(self.board.board_state["castling"], "-")

    def test_move_king_castling_forfeit(self):
        self.board = Board(CASTLING_FEN)

        self.board.move(start_coord=(6, 4), end_coord=(5, 4))
        self.board.move(start_coord=(1, 4), end_coord=(2, 4))
        self.board.move(start_coord=(7, 4), end_coord=(6, 4))
        self.board.move(start_coord=(0, 4), end_coord=(1, 4))
        self.board.move(start_coord=(6, 4), end_coord=(7, 4))
        self.board.move(start_coord=(1, 4), end_coord=(0, 4))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 6))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 2))

        self.board.move(start_coord=(7, 4), end_coord=(6, 4))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 6))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        self.board.move(start_coord=(0, 4), end_coord=(1, 4))


    def test_move_castle_through_check_1(self):
        self.board = Board(ILLEGAL_CASTLING_THROUGH_CHECK_1_FEN)

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 6))

        self.board.move(start_coord=(7, 7), end_coord=(6, 7))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 6))

        self.board.move(start_coord=(0, 7), end_coord=(1, 7))


    def test_move_castle_through_check_2(self):
        self.board = Board(ILLEGAL_CASTLING_THROUGH_CHECK_2_FEN)

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 6))

        self.board.move(start_coord=(7, 7), end_coord=(6, 7))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 6))

        self.board.move(start_coord=(0, 7), end_coord=(1, 7))


    def test_move_castle_in_check_white(self):
        self.board = Board(ILLEGAL_CASTLING_WHITE_IN_CHECK)

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(7, 4), end_coord=(7, 6))


    def test_move_castle_in_check_black(self):
        self.board = Board(ILLEGAL_CASTLING_BLACK_IN_CHECK)

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 2))

        with self.assertRaises(ValueError):
            self.board.move(start_coord=(0, 4), end_coord=(0, 6))
# ============================== END TEST move() ==============================

    # Test board visualization
    def test_str_conversion(self):
        print(str(self.board))
        print("------")
        print(STARTING_POSITION_STRING_OUTPUT.strip())

        self.assertEqual(
            str(self.board).strip(),
            STARTING_POSITION_STRING_OUTPUT.strip()
        )

if __name__=="__main__":
    unittest.main()
