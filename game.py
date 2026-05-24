import time
from pyray import *
from dictionary import load_word_list
from dice import generate_random_board, build_board_from_seed
from settings import roundCountdownTime, roundTime


class BoggleGame:
    def __init__(self):
        self.valid_words = load_word_list()
        self.reset()

    def reset(self):
        self.seed = ""
        self.output = []
        self.current_word = ""
        self.selected_positions = []
        self.words_guessed = []
        self.invalid_word_message = ""
        self.invalid_message_time = 0.0
        self.seed_lockout_time = 0.0
        self.countdown_timer = 0.0
        self.round_timer = 0.0
        self.last_known_position = None

    @property
    def has_board(self):
        return len(self.output) == 25

    def start_new_board(self):
        self.seed, self.output = generate_random_board()
        self.countdown_timer = time.time() + roundCountdownTime
        self.round_timer = time.time() + roundTime + roundCountdownTime
        self.current_word = ""
        self.selected_positions = []
        self.words_guessed = []
        self.invalid_word_message = ""
        self.invalid_message_time = 0.0
        self.last_known_position = None

    def start_board_with_seed(self, seed):
        self.output = build_board_from_seed(seed)
        self.seed = seed
        self.countdown_timer = time.time() + roundCountdownTime
        self.round_timer = time.time() + roundTime + roundCountdownTime
        self.current_word = ""
        self.selected_positions = []
        self.words_guessed = []
        self.invalid_word_message = ""
        self.invalid_message_time = 0.0
        self.last_known_position = None

    def is_countdown_active(self):
        return self.has_board and time.time() < self.countdown_timer

    def get_time_remaining(self):
        return max(0.0, self.round_timer - time.time())

    def get_countdown_remaining(self):
        return max(0.0, self.countdown_timer - time.time())

    def is_game_active(self):
        return self.has_board and time.time() >= self.countdown_timer

    def is_seed_button_ready(self):
        return self.seed_lockout_time < time.time()

    def build_word_from_positions(self):
        return "".join(self.output[pos[0] * 5 + pos[1]] for pos in self.selected_positions)

    def get_letter_center(self, coord):
        from settings import partitioned_fifths, board_height, y_letter_offset

        return Vector2(
            int(coord[0] * partitioned_fifths + (partitioned_fifths * 0.5)),
            int(coord[1] * partitioned_fifths + (y_letter_offset * 0.8) + (board_height * 0.2) / 3.56),
        )

    def get_grid_coords(self):
        from settings import partitioned_fifths, board_height, y_letter_offset

        for x in range(5):
            for y in range(5):
                pos_x = int(x * partitioned_fifths + (partitioned_fifths * 0.5))
                pos_y = int(y * partitioned_fifths + (y_letter_offset * 0.8) + (board_height * 0.2) / 3.56)
                if check_collision_point_circle(get_mouse_position(), (pos_x, pos_y), 55):
                    return (x, y)
        return None

    def get_letter_at_position(self):
        coords = self.get_grid_coords()
        if coords is not None:
            return self.output[coords[0] * 5 + coords[1]]
        return ""

    def is_adjacent(self, coord, reference):
        if reference is None:
            return False
        return abs(coord[0] - reference[0]) <= 1 and abs(coord[1] - reference[1]) <= 1

    def update_selection(self):
        if not self.output or not is_mouse_button_down(0):
            return

        coord = self.get_grid_coords()
        if coord is None:
            return

        if not self.selected_positions:
            letter = self.get_letter_at_position()
            if letter:
                self.selected_positions.append(coord)
                self.current_word = self.build_word_from_positions()
                self.last_known_position = coord
            return

        if len(self.selected_positions) >= 2 and coord == self.selected_positions[-2]:
            self.selected_positions.pop()
            self.current_word = self.build_word_from_positions()
            self.last_known_position = self.selected_positions[-1] if self.selected_positions else None
        elif coord not in self.selected_positions and self.is_adjacent(coord, self.last_known_position):
            self.selected_positions.append(coord)
            self.current_word = self.build_word_from_positions()
            self.last_known_position = coord

    def submit_word(self):
        if not self.output or self.current_word == "" or not is_mouse_button_released(0):
            return

        candidate = self.current_word.upper()
        if candidate in self.valid_words and len(candidate) >= 4 and candidate not in self.words_guessed:
            self.words_guessed.append(candidate)
        elif candidate in self.words_guessed:
            self.invalid_word_message = "Word already\nguessed"
            self.invalid_message_time = time.time()
        elif len(candidate) < 4:
            self.invalid_word_message = "Word must\nbe at least\n4 letters"
            self.invalid_message_time = time.time()
        else:
            self.invalid_word_message = "Not a\nvalid word"
            self.invalid_message_time = time.time()

        self.current_word = ""
        self.selected_positions.clear()
        self.last_known_position = None

    def update(self):
        self.update_selection()
        self.submit_word()

    def seed_is_valid(self, seed):
        return len(seed) == 75 and seed.isdigit()
