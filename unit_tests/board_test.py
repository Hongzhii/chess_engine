import unittest

from src.board import Board
from resources.FENs import FOURKNIGHTS_FEN, LONDON_FEN

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


    # FEN constructor verification --> check board state is loaded correctly
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


    # Check if overlap detection function works properly
    def test_overlap_check(self):
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


    # Test the move() method
    def test_move(self):
        """
        This is a high level test verifying the functionality of the move() method.

        Other involved methods/functionalities:
            board.py
                handle_pawn_moves()
                handle_king_moves()
                `to_move` and `moves` board state attributes
            piece_handler.py
                get_moves()
            bitboard.py
                get()
        """

        # Test regular moves
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
            self.assertEqual(v.bitboard, EXPECTED_4KNIGHTS_WHITE[k])
        for k, v in self.board.black_positions.items():
            self.assertEqual(v.bitboard, EXPECTED_4KNIGHTS_BLACK[k])

        
        # Test en passant moves

        # Test castling


    # show()

if __name__=="__main__":
    unittest.main()
