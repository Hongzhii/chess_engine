import unittest

from src.bitboard import BitBoard

class TestBitBoard(unittest.TestCase):
    def setUp(self):
        """
        Functions as __init__() method. However, this method is run every time a new
        testcase method is called. This ensures that each testcase has a clean instance
        """

        self.bitboard = BitBoard()


    def test_set_method(self):
        self.bitboard.set(0, 0)
        self.bitboard.set(7, 7)
        self.bitboard.set(0, 7)
        self.bitboard.set(7, 0)
        self.bitboard.set(4, 4)

        expected_val = "".join([
            "10000001",
            "00000000",
            "00000000",
            "00000000",
            "00001000",
            "00000000",
            "00000000",
            "10000001"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(self.bitboard.bitboard, expected_val)

    def test_unset_method(self):
        self.bitboard.unset(0, 0)

        initial_state = "".join([
            "10000001",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "10000001"
        ])
        self.bitboard.bitboard = int(initial_state, 2)

        self.bitboard.unset(0, 0)
        self.bitboard.unset(7, 0)

        expected_val = "".join([
            "00000001",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000001"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(self.bitboard.bitboard, expected_val)

    def test_copy_constructor(self):
        initial_state = "".join([
            "10000001",
            "00000000",
            "00000000",
            "00001000",
            "10000000",
            "00000001",
            "00000000",
            "10000001"
        ])
        self.bitboard.bitboard = int(initial_state, 2)

        new_bitboard = BitBoard(bitboard=self.bitboard)

        self.assertEqual(self.bitboard.bitboard, new_bitboard.bitboard)

    def test_coordinate_constructor(self):
        test_coords = [
            (0, 0),
            (0, 7),
            (7, 0),
            (7, 7),
            (4, 4),
            (3, 3),
            (2, 5),
            (6, 1),
            (8, 8),  # Invalid coordinate
            (-1, -1),  # Invalid coordinate
            (99, 5),  # Invalid coordinate
            (5, 99)  # Invalid coordinate
        ]
        new_bitboard = BitBoard(coordinates=test_coords)

        expected_val = "".join([
            "10000001",
            "00000000",
            "00000100",
            "00010000",
            "00001000",
            "00000000",
            "01000000",
            "10000001"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(new_bitboard.bitboard, expected_val)

    def test_inplace_add_method(self):
        initial_val = "".join([
            "10000000",
            "01000000",
            "00100000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
        ])
        initial_val = int(initial_val, 2)

        add_val = "".join([
            "00000000",
            "00000000",
            "00000000",
            "00010000",
            "00001000",
            "00000100",
            "00000000",
            "00000000"
        ])
        add_val = int(add_val, 2)

        bitboard = BitBoard()
        bitboard.bitboard = initial_val

        add_bitboard = BitBoard()
        add_bitboard.bitboard = add_val

        bitboard += add_bitboard

        expected_val = "".join([
            "10000000",
            "01000000",
            "00100000",
            "00010000",
            "00001000",
            "00000100",
            "00000000",
            "00000000"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(bitboard.bitboard, expected_val)

if __name__=="__main__":
    unittest.main()
