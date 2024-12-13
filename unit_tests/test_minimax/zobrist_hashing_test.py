import unittest
import json

class TestZobristHashes(unittest.TestCase):
    def setUp(self):
        with open("/Users/hongzhiee/Desktop/Projects/chess_engine/resources/hash_keys.json") as f:
            self.hash_key_mapping = json.load(f)

    def test_duplicate_keys(self):
        hash_keys = []

        for _, square_dict in self.hash_key_mapping["position"].items():
            for _, hash_key in square_dict.items():
                hash_keys.append(hash_key)

        for _, hash_key in self.hash_key_mapping["castling"].items():
            hash_keys.append(hash_key)

        for _, hash_key in self.hash_key_mapping["en_passant"].items():
            hash_keys.append(hash_key)

        hash_keys.append(self.hash_key_mapping["to_move"])

        print(hash_keys)

        self.assertTrue(len(set(hash_keys)) == len(hash_keys))
