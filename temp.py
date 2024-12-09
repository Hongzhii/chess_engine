from src.bitboard import BitBoard
from src.board import Board
from resources import FENs

board = Board(fen_string=FENs.ILLEGAL_CASTLING_BLACK_IN_CHECK)

print(board.board_state["castling"])
