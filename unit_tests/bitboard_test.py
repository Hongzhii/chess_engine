import unittest

from src.bitboard import BitBoard

class TestBitBoard(unittest.TestCase):
    def setUp(self):
        """
        Functions as __init__() method. However, this method is run every time a new
        testcase method is called. This ensures that each testcase has a clean instance
        """

        self.bitboard = BitBoard()

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

    def test_set(self):
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

    def test_unset(self):
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

    def test_get_coordinates(self):
        self.bitboard.bitboard = int("".join([
            "10000001",
            "00100000",
            "00000100",
            "00000001",
            "00100000",
            "10000010",
            "00000000",
            "10000001",
        ]), 2)
        expected_output = [
            (0, 0), (0, 7),
            (1, 2),
            (2, 5),
            (3, 7),
            (4, 2),
            (5, 0), (5, 6),
            (7, 0), (7, 7)
        ]

        coords = self.bitboard.get_coordinates()

        self.assertEqual(coords, expected_output)

    def test_add(self):
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
            "00100000",
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

        # Make a copy for equality verification check
        original_bitboard = BitBoard()
        original_bitboard.bitboard = bitboard.bitboard
        original_add_bitboard = BitBoard()
        original_add_bitboard.bitboard = add_bitboard.bitboard

        new_bitboard = bitboard + add_bitboard

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

        self.assertEqual(new_bitboard.bitboard, expected_val)

        # Original values should not be changed
        self.assertEqual(bitboard.bitboard, original_bitboard.bitboard)
        self.assertEqual(add_bitboard.bitboard, original_add_bitboard.bitboard)

    def test_inplace_add(self):
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
            "00100000",
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

        # Make a copy for equality verification check
        original_bitboard = BitBoard()
        original_bitboard.bitboard = bitboard.bitboard
        original_add_bitboard = BitBoard()
        original_add_bitboard.bitboard = add_bitboard.bitboard

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

        # Original value for bitboard should be different
        self.assertNotEqual(bitboard.bitboard, original_bitboard.bitboard)
        self.assertEqual(add_bitboard.bitboard, original_add_bitboard.bitboard)

    def test_minus(self):
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

        minus_val = "".join([
            "00000000",
            "00000000",
            "00100000",
            "00010000",
            "00001000",
            "00000100",
            "00000000",
            "00000000"
        ])
        minus = int(minus_val, 2)

        bitboard = BitBoard()
        bitboard.bitboard = initial_val

        minus_bitboard = BitBoard()
        minus_bitboard.bitboard = minus

        new_bitboard = bitboard - minus_bitboard

        expected_val = "".join([
            "10000000",
            "01000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(new_bitboard.bitboard, expected_val)

    def test_inplace_minus(self):
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

        minus_val = "".join([
            "00000000",
            "00000000",
            "00100000",
            "00010000",
            "00001000",
            "00000100",
            "00000000",
            "00000000"
        ])
        minus_val = int(minus_val, 2)

        bitboard = BitBoard()
        bitboard.bitboard = initial_val

        minus_bitboard = BitBoard()
        minus_bitboard.bitboard = minus_val

        # Make a copy for equality verification check
        original_bitboard = BitBoard()
        original_bitboard.bitboard = bitboard.bitboard
        original_minus_bitboard = BitBoard()
        original_minus_bitboard.bitboard = minus_bitboard.bitboard

        bitboard -= minus_bitboard

        expected_val = "".join([
            "10000000",
            "01000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000",
            "00000000"
        ])
        expected_val = int(expected_val, 2)

        self.assertEqual(bitboard.bitboard, expected_val)

        # Original value for bitboard should be different
        self.assertNotEqual(bitboard.bitboard, original_bitboard.bitboard)
        self.assertEqual(minus_bitboard.bitboard, original_minus_bitboard.bitboard)


if __name__=="__main__":
    unittest.main()
