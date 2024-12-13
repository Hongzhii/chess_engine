import unittest

from src.chess_board import parsers

class TestParser(unittest.TestCase):
    def test_alphanumeric(self):
        position_input = "a1"
        expected_output = ((7, 0), None)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "h8"
        expected_output = ((0, 7), None)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "e4"
        expected_output = ((4, 4), None)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "e4=Q"
        expected_output = ((4, 4), "q")
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "e4=q"
        expected_output = ((4, 4), "q")
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "e8=z"
        expected_output = ((0, 4), "z")
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )
