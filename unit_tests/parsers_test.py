import unittest

from src import parsers

class TestParser(unittest.TestCase):
    def test_alphanumeric(self):
        position_input = "a1"
        expected_output = (7, 0)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "h8"
        expected_output = (0, 7)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )

        position_input = "e4"
        expected_output = (4, 4)
        self.assertEqual(
            parsers.alphanumeric_to_index(position_input), expected_output
        )
