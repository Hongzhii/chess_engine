import parsers
import os

from board import Board

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
        user_input = input("Enter piece coordinates:\n")

        if(user_input == "q"):
            break

        try:
            start_coord = parsers.alphanumeric_to_index(user_input.lower())
        except ValueError as e:
            error_message = e
            continue

        if not friendly_pieces.get(*start_coord):
            error_message = "Please select a valid friendly piece"
            continue

        user_input = input("Enter destination coordinates:\n")

        try:
            end_coord = parsers.alphanumeric_to_index(user_input.lower())
            board.move(start_coord, end_coord)
        except ValueError as e:
            error_message = e
            continue

        if(user_input == "q"):
            break
