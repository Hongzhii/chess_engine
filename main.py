from src.chess_board.board import Board
from src.chess_board.parsers import alphanumeric_to_index

from resources import FENs

def get_debug_board():
    return Board(FENs.FOURKNIGHTS_FEN)

if __name__ == "__main__":
    """
    Logic for the main game loop
    """

    board = Board()
    ERROR_MESSAGE = None

    while True:
        # os.system("clear")

        print(board)

        to_move = board.board_state["to_move"]
        COLOR = "Black" if to_move == -1 else "White"

        friendly_pieces = board.get_color_bitboard(to_move)

        print("Enter 'q' to quit")

        print("="*40)

        if ERROR_MESSAGE is not None:
            print(ERROR_MESSAGE)
            ERROR_MESSAGE = None

        print(f"{COLOR} to move")

        while True:
            target_coord = input("Enter target square:\n")
            if target_coord == "q":
                break
            if target_coord == "debug":
                break
            try:
                target_coord, _ = alphanumeric_to_index(target_coord)
                break
            except ValueError as e:
                print(e)

        if target_coord == "q":
            break
        if target_coord == "debug":
            board = get_debug_board()
            continue

        while True:
            destination_coord = input("Enter destination square:\n")
            if destination_coord == "q":
                break
            if destination_coord == "debug":
                break
            try:
                destination_coord, promotion_piece_type = alphanumeric_to_index(destination_coord)
                break
            except ValueError as e:
                print(e)

        if destination_coord == "q":
            break
        if destination_coord == "debug":
            board = get_debug_board()
            continue

        try:
            board.move(
                start_coord=target_coord,
                end_coord=destination_coord,
                promotion_piece_type=promotion_piece_type
            )
        except ValueError as e:
            ERROR_MESSAGE = str(e)
