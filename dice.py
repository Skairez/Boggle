import random

# 25 Boggle dice, each with 6 faces.
dice = {
    0: ['F', 'R', 'Y', 'S', 'P', 'I'],
    1: ['A', 'A', 'F', 'S', 'I', 'R'],
    2: ['H', 'O', 'H', 'D', 'L', 'N'],
    3: ['E', 'E', 'E', 'A', 'E', 'A'],
    4: ['E', 'T', 'C', 'S', 'C', 'N'],
    5: ['M', 'E', 'O', 'T', 'T', 'T'],
    6: ['T', 'O', 'O', 'O', 'T', 'U'],
    7: ['N', 'N', 'N', 'A', 'D', 'E'],
    8: ['E', 'E', 'E', 'E', 'A', 'M'],
    9: ['N', 'D', 'D', 'T', 'O', 'H'],
    10: ['C', 'P', 'I', 'E', 'S', 'T'],
    11: ['O', 'O', 'U', 'W', 'T', 'N'],
    12: ['TH', 'IN', 'QU', 'HE', 'AN', 'ER'],
    13: ['U', 'E', 'N', 'S', 'S', 'S'],
    14: ['O', 'R', 'D', 'H', 'N', 'L'],
    15: ['N', 'M', 'N', 'A', 'E', 'G'],
    16: ['Z', 'B', 'QU', 'J', 'X', 'K'],
    17: ['S', 'A', 'Y', 'F', 'R', 'I'],
    18: ['A', 'A', 'F', 'A', 'R', 'A'],
    19: ['P', 'W', 'R', 'G', 'V', 'R'],
    20: ['T', 'I', 'T', 'I', 'I', 'E'],
    21: ['P', 'E', 'L', 'C', 'T', 'I'],
    22: ['D', 'H', 'O', 'R', 'L', 'H'],
    23: ['E', 'U', 'A', 'G', 'M', 'E'],
    24: ['C', 'T', 'I', 'L', 'I', 'E'],
}


def generate_seed():
    return "".join(f"{random.randint(0, 24):02d}{random.randint(0, 5)}" for _ in range(25))


def build_board_from_seed(seed):
    return [dice[int(seed[i:i+2])][int(seed[i+2])] for i in range(0, len(seed), 3)]


def generate_random_board():
    seed = generate_seed()
    return seed, build_board_from_seed(seed)
