from src.chess_board.bitboard import BitBoard
from src.chess_board.board import Board
from resources import FENs

board = Board(fen_string=FENs.ILLEGAL_CASTLING_BLACK_IN_CHECK)
# board = Board()

board.get_legal_moves()
