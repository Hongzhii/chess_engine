import unittest

from src import parsers

class TestParser(unittest.TestCase):
    def test_alphanumeric(self):
        position_input = "a1"
        expected_output = (0, 0)
        self.assertTrue(
            parsers.alphanumeric_to_index(position_input, expected_output)
        )

        position_input = "h8"
        expected_output = (7, 7)
        self.assertTrue(
            parsers.alphanumeric_to_index(position_input, expected_output)
        )

        position_input = "e4"
        expected_output = (4, 3)
        self.assertTrue(
            parsers.alphanumeric_to_index(position_input, expected_output)
        )
