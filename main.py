import os
import parsers

from board import Board
from parsers import alphanumeric_to_index

import FENs

def get_debug_board():
    return Board(FENs.FOURKNIGHTS_FEN)

if __name__ == "__main__":
    """
    Logic for the main game loop
    """

    board = Board()
    error_message = None

    while True:
        # os.system("clear")

        board.show()

        to_move = board.to_move
        color = "Black" if to_move == -1 else "White"

        friendly_pieces = board.get_color_bitboard(to_move)

        print("King-side castle: O-O")
        print("Queen-side castle: O-O-O")
        print("Enter 'q' to quit")

        print("="*40)

        if error_message is not None:
            print(error_message)
            error_message = None

        print(f"{color} to move")

        while True:
            target_coord = input("Enter target square:\n")
            if target_coord == "q":
                break
            elif target_coord == "debug":
                break
            try:
                target_coord = alphanumeric_to_index(target_coord)
                break
            except ValueError as e:
                print(e)

        if target_coord == "q":
            break
        elif target_coord == "debug":
            board = get_debug_board()
            continue

        while True:
            destination_coord = input("Enter destination square:\n")
            if destination_coord == "q":
                break
            elif destination_coord == "debug":
                break
            try:
                destination_coord = alphanumeric_to_index(destination_coord)
                break
            except ValueError as e:
                print(e)

        if destination_coord == "q":
            break
        elif destination_coord == "debug":
            board = get_debug_board()
            continue

        try:
            board.move(
                start_coord=target_coord,
                end_coord=destination_coord
            )
        except ValueError as e:
            error_message = str(e)

        
