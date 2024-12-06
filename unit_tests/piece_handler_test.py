import unittest

from src import piece_handler
from src.board import Board

from resources import FENs

class TestPieceHandler(unittest.TestCase):
    def test_get_pawn_moves(self):
        board = Board(FENs.SURROUND_PAWN_FRIENDLY)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)

        board = Board(FENs.SURROUND_PAWN_OPPONENT)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00010100",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_PAWN_FRIENDLY)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00001000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_PAWN_OPPONENT)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00001000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)

        board = Board(FENs.FREE_PAWN)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00001000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)

        board = Board(FENs.FREE_PAWN_DOUBLE_SQUARE)
        pawn_moves = piece_handler._get_pawn_moves(
            board=board,
            position=(6, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00001000",
            "00001000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(pawn_moves.bitboard, expected)


    def test_get_knight_moves(self):
        board = Board(FENs.SURROUND_KNIGHT_FRIENDLY)
        knight_moves = piece_handler._get_knight_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00010100",
            "00100010",
            "00000000",
            "00100010",
            "00010100",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(knight_moves.bitboard, expected)

        board = Board(FENs.SURROUND_KNIGHT_OPPONENT)
        knight_moves = piece_handler._get_knight_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00010100",
            "00100010",
            "00000000",
            "00100010",
            "00010100",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(knight_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_KNIGHT_FRIENDLY)
        knight_moves = piece_handler._get_knight_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(knight_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_KNIGHT_OPPONENT)
        knight_moves = piece_handler._get_knight_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00010100",
            "00100010",
            "00000000",
            "00100010",
            "00010100",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(knight_moves.bitboard, expected)

        board = Board(FENs.FREE_KNIGHT)
        knight_moves = piece_handler._get_knight_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00010100",
            "00100010",
            "00000000",
            "00100010",
            "00010100",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(knight_moves.bitboard, expected)


    def test_get_bishop_moves(self):
        board = Board(FENs.SURROUND_BISHOP_FRIENDLY)
        bishop_moves = piece_handler._get_bishop_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(bishop_moves.bitboard, expected)

        board = Board(FENs.SURROUND_BISHOP_OPPONENT)
        bishop_moves = piece_handler._get_bishop_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00010100",
            "00000000",
            "00010100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(bishop_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_BISHOP_FRIENDLY)
        bishop_moves = piece_handler._get_bishop_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00010100",
            "00000000",
            "00010100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(bishop_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_BISHOP_OPPONENT)
        bishop_moves = piece_handler._get_bishop_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00100010",
            "00010100",
            "00000000",
            "00010100",
            "00100010",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(bishop_moves.bitboard, expected)

        board = Board(FENs.FREE_BISHOP)
        bishop_moves = piece_handler._get_bishop_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "01000001",
            "00100010",
            "00010100",
            "00000000",
            "00010100",
            "00100010",
            "01000001",
            "10000000",
        ]), 2)
        self.assertEqual(bishop_moves.bitboard, expected)


    def test_get_rook_moves(self):
        board = Board(FENs.SURROUND_ROOK_FRIENDLY)
        rook_moves = piece_handler._get_rook_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(rook_moves.bitboard, expected)

        board = Board(FENs.SURROUND_ROOK_OPPONENT)
        rook_moves = piece_handler._get_rook_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00001000",
            "00010100",
            "00001000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(rook_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_ROOK_FRIENDLY)
        rook_moves = piece_handler._get_rook_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00001000",
            "00010100",
            "00001000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(rook_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_ROOK_OPPONENT)
        rook_moves = piece_handler._get_rook_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00001000",
            "00001000",
            "00110110",
            "00001000",
            "00001000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(rook_moves.bitboard, expected)

        board = Board(FENs.FREE_ROOK)
        rook_moves = piece_handler._get_rook_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00001000",
            "00001000",
            "00001000",
            "11110111",
            "00001000",
            "00001000",
            "00001000",
            "00001000",
        ]), 2)
        self.assertEqual(rook_moves.bitboard, expected)


    def test_get_queen_moves(self):
        board = Board(FENs.SURROUND_QUEEN_FRIENDLY)
        queen_moves = piece_handler._get_queen_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(queen_moves.bitboard, expected)

        board = Board(FENs.SURROUND_QUEEN_OPPONENT)
        queen_moves = piece_handler._get_queen_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(queen_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_QUEEN_FRIENDLY)
        queen_moves = piece_handler._get_queen_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(queen_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_QUEEN_OPPONENT)
        queen_moves = piece_handler._get_queen_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00101010",
            "00011100",
            "00110110",
            "00011100",
            "00101010",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(queen_moves.bitboard, expected)

        board = Board(FENs.FREE_QUEEN)
        queen_moves = piece_handler._get_queen_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "01001001",
            "00101010",
            "00011100",
            "11110111",
            "00011100",
            "00101010",
            "01001001",
            "10001000",
        ]), 2)
        self.assertEqual(queen_moves.bitboard, expected)

    def test_get_king_moves(self):
        board = Board(FENs.SURROUND_KING_FRIENDLY)
        king_moves = piece_handler._get_king_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(king_moves.bitboard, expected)

        board = Board(FENs.SURROUND_KING_OPPONENT)
        king_moves = piece_handler._get_king_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(king_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_KING_FRIENDLY)
        king_moves = piece_handler._get_king_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(king_moves.bitboard, expected)

        board = Board(FENs.SURROUND_GAP_KING_OPPONENT)
        king_moves = piece_handler._get_king_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(king_moves.bitboard, expected)

        board = Board(FENs.FREE_KING)
        king_moves = piece_handler._get_king_moves(
            board=board,
            position=(3, 4)
        )
        expected = int("".join([
            "00000000",
            "00000000",
            "00011100",
            "00010100",
            "00011100",
            "00000000",
            "00000000",
            "00000000",
        ]), 2)
        self.assertEqual(king_moves.bitboard, expected)

    # Test in-check detection method
    def test_in_check(self):
        """
        This test case tests the functionality of the in_check() method.

        Other involved methods/functionalities:
            piece_handler.py
                _get_{piece}_moves.py
        """
        board = Board(FENs.ILLEGAL_CASTLING_WHITE_IN_CHECK)
        self.assertTrue(piece_handler.in_check(board))

        board = Board(FENs.ILLEGAL_CASTLING_BLACK_IN_CHECK)
        self.assertTrue(piece_handler.in_check(board))

        board = Board()
        self.assertFalse(piece_handler.in_check(board))

        board.move((6, 4), (4, 4))
        self.assertFalse(piece_handler.in_check(board))
