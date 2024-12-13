import random
import json

def generate_hash_keys():
    position_map = {}

    for i in range(8):
        for j in range(8):
            coordinate_map = {}

            for piece in ["p", "n", "b", "r", "q", "k"]:
                coordinate_map[piece] = random.randint(1, 2**64)

            position_map[f"{i}{j}"] = coordinate_map

    castling_map = {}

    for config in [
        "-", "---q", "--k-", "--kq",
        "-Q--", "-Q-q", "-Qk-", "-Qkq",
        "K---", "K--q", "K-k-", "K-kq",
        "KQ--", "KQ-q", "KQk-", "KQkq",
    ]:
        castling_map[config] = random.randint(1, 2**64)

    en_passant_map = {}

    for file in range(8):
        en_passant_map[str(file)] = random.randint(1, 2**64)

    hash_map = {
        "position": position_map,
        "castling": castling_map,
        "en_passant": en_passant_map,
        "to_move": random.randint(1, 2**64),
    }

    with open("/Users/hongzhiee/Desktop/Projects/chess_engine/resources/hash_keys.json", "w") as f:
        json.dump(hash_map, f)


if __name__ == "__main__":
    generate_hash_keys()
