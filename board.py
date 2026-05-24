from pyray import *
import time
import pyperclip

import settings
from button import Button
from game import BoggleGame


def create_buttons(new_game_font, new_game_font_size, timer_font, timer_font_size):
    x = settings.button_x
    width = settings.button_width
    height = settings.button_height

    new_game_button = Button(
        x,
        int(settings.board_height / 16),
        width,
        height,
        "New Game",
        new_game_font,
        new_game_font_size,
        color=settings.button_default_color,
    )

    timer_button = Button(
        x,
        new_game_button.bounds.y + height + 20,
        width,
        height,
        "00:00",
        timer_font,
        timer_font_size,
        color=YELLOW,
    )

    seed_button = Button(
        x,
        int(settings.board_height * 0.75),
        width,
        height,
        "Copy Seed",
        new_game_font,
        new_game_font_size,
        color=settings.button_default_color,
    )

    return new_game_button, timer_button, seed_button


def draw_countdown_overlay(countdown_seconds):
    draw_rectangle_gradient_ex(
        Rectangle(0, 0, settings.board_width, settings.board_height),
        *settings.countdownBackgroundColors,
    )

    if countdown_seconds > 3:
        label = "Ready?"
        offset = 0.15
    elif countdown_seconds > 1:
        label = "Set..."
        offset = 0.3
    else:
        label = "Go!"
        offset = 0.35

    draw_text_ex(
        countdownFont,
        label,
        Vector2(int(settings.board_width * offset), int(settings.board_height / 2 - (countdownFontSize * 0.5))),
        countdownFontSize,
        1,
        BLACK,
    )


def draw_board_letters(game):
    i = 0
    for x in range(5):
        for y in range(5):
            output_current = game.output[i]
            if output_current == "IN":
                pos = Vector2(
                    int(x * settings.partitioned_fifths + (settings.partitioned_fifths * 0.5) - (boggleFontSize * 0.35)),
                    int(y * settings.partitioned_fifths + (settings.y_letter_offset * 0.8)),
                )
            elif len(output_current) > 1:
                pos = Vector2(
                    int(x * settings.partitioned_fifths + (settings.partitioned_fifths * 0.5) - (boggleFontSize * 0.52)),
                    int(y * settings.partitioned_fifths + (settings.y_letter_offset * 0.8)),
                )
            elif output_current == "I":
                pos = Vector2(
                    int(x * settings.partitioned_fifths + (settings.partitioned_fifths * 0.5) - (boggleFontSize * 0.11)),
                    int(y * settings.partitioned_fifths + (settings.y_letter_offset * 0.8)),
                )
            else:
                pos = Vector2(
                    int(x * settings.partitioned_fifths + (settings.partitioned_fifths * 0.5) - (boggleFontSize * 0.24)),
                    int(y * settings.partitioned_fifths + (settings.y_letter_offset * 0.8)),
                )

            letter_die_face = Rectangle(
                x * settings.partitioned_fifths + (settings.partitioned_fifths * 0.05),
                y * settings.partitioned_fifths + (settings.partitioned_fifths * 0.05),
                settings.partitioned_fifths * 0.9,
                settings.partitioned_fifths * 0.9,
            )

            letter_color = (
                settings.selected_die_color
                if (x, y) in game.selected_positions
                else settings.dieColor
            )

            draw_rectangle_rounded(letter_die_face, 0.5, 10, letter_color)
            draw_text_ex(boardFont, output_current, pos, boggleFontSize, 0, BLACK)
            i += 1


def draw_board_grid():
    for x in range(5):
        draw_line(
            int(x * settings.partitioned_fifths + settings.partitioned_fifths),
            0,
            int(x * settings.partitioned_fifths + settings.partitioned_fifths),
            settings.board_height,
            BLACK,
        )
    for y in range(5):
        draw_line(
            0,
            int(y * settings.partitioned_fifths + settings.partitioned_fifths),
            settings.board_width,
            int(y * settings.partitioned_fifths + settings.partitioned_fifths),
            BLACK,
        )


def draw_guess_list(game, start_y):
    for i, guessed_word in enumerate(game.words_guessed):
        draw_text_ex(
            guessesFont,
            f"{i}. {guessed_word}",
            Vector2(settings.button_x, start_y + i * guessesFontSize),
            guessesFontSize,
            1,
            BLACK,
        )


def draw_invalid_message(game, bounds):
    if not game.invalid_word_message:
        return
    if time.time() - game.invalid_message_time < settings.INVALID_MESSAGE_DURATION:
        draw_text_ex(
            guessesFont,
            game.invalid_word_message,
            Vector2(bounds.x, bounds.y),
            invalidMessageFontSize,
            1,
            settings.warning_color,
        )
    else:
        game.invalid_word_message = ""


def draw_word_path(game):
    if len(game.selected_positions) >= 2:
        for start, end in zip(game.selected_positions, game.selected_positions[1:]):
            draw_line_ex(game.get_letter_center(start), game.get_letter_center(end), 12, RED)

    if is_mouse_button_down(0) and game.selected_positions:
        last_pos = game.get_letter_center(game.selected_positions[-1])
        draw_line_ex(last_pos, get_mouse_position(), 6, RED)


def main():
    global boggleFontSize, newGameFontSize, timerFontSize, guessesFontSize, countdownFontSize, invalidMessageFontSize, seedSelectFontSize
    init_window(settings.window_width, settings.window_height, "Boggle")

    boggleFontSize = int(settings.board_height * 0.15)
    newGameFontSize = int(settings.board_height * 0.035)
    timerFontSize = int(settings.board_height * 0.05)
    guessesFontSize = int(settings.board_height * 0.03)
    countdownFontSize = int(settings.board_height * 0.25)
    invalidMessageFontSize = int(settings.board_height * 0.04)
    seedSelectFontSize = int(settings.board_height * 0.1)

    global boardFont, newGameFont, timerFont, guessesFont, countdownFont, invalidMessageFont, seedSelectFont
    boardFont = load_font_ex("PlatNomor.ttf", boggleFontSize, None, 95)
    newGameFont = load_font_ex("PlatNomor.ttf", newGameFontSize, None, 95)
    timerFont = load_font_ex("PlatNomor.ttf", timerFontSize, None, 95)
    guessesFont = load_font_ex("PlatNomor.ttf", guessesFontSize, None, 95)
    countdownFont = load_font_ex("PlatNomor.ttf", countdownFontSize, None, 95)
    invalidMessageFont = load_font_ex("PlatNomor.ttf", invalidMessageFontSize, None, 95)
    seedSelectFont = load_font_ex("PlatNomor.ttf", seedSelectFontSize, None, 95)

    game = BoggleGame()
    new_game_button, timer_button, seed_button = create_buttons(
        newGameFont,
        newGameFontSize,
        timerFont,
        timerFontSize,
    )

    current_word_box_bounds = Rectangle(
        settings.button_x,
        timer_button.bounds.y + timer_button.bounds.height + 20,
        settings.button_width,
        int(settings.board_height * 0.12),
    )

    seed_feedback = ""
    seed_feedback_time = 0.0

    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)

        if not game.has_board:
            generate_bounds = Rectangle(settings.board_width * 0.1, settings.board_height * 0.1, settings.board_width * 0.9, settings.board_height * 0.4)
            paste_bounds = Rectangle(settings.board_width * 0.1, settings.board_height * 0.55, settings.board_width * 0.9, settings.board_height * 0.4)

            draw_rectangle_rounded(generate_bounds, 0.5, 10, LIGHTGRAY)
            draw_text_ex(
                seedSelectFont,
                "Click to\nGenerate Board",
                Vector2(int(settings.board_width * 0.2), int(settings.board_height * 0.2)),
                seedSelectFontSize,
                1,
                BLACK,
            )

            draw_rectangle_rounded(paste_bounds, 0.5, 10, LIGHTGRAY)
            draw_text_ex(
                seedSelectFont,
                "Click to\nPaste Seed",
                Vector2(int(settings.board_width * 0.2), int(settings.board_height * 0.65)),
                seedSelectFontSize,
                1,
                BLACK,
            )

            if is_mouse_button_pressed(0) and check_collision_point_rec(get_mouse_position(), generate_bounds):
                game.start_new_board()
                time.sleep(0.2)

            if is_mouse_button_pressed(0) and check_collision_point_rec(get_mouse_position(), paste_bounds):
                pasted = input("Enter seed: ")
                if not game.seed_is_valid(pasted):
                    seed_feedback = "Invalid seed!"
                    seed_feedback_time = time.time()
                else:
                    game.start_board_with_seed(pasted)
                    seed_feedback = "Seed pasted!"
                    seed_feedback_time = time.time()
                time.sleep(0.2)

            if seed_feedback and time.time() - seed_feedback_time < settings.INVALID_MESSAGE_DURATION:
                draw_text_ex(
                    seedSelectFont,
                    seed_feedback,
                    Vector2(int(settings.board_width * 0.1), int(settings.board_height * 0.7)),
                    seedSelectFontSize,
                    1,
                    BLACK,
                )
        else:
            if game.is_countdown_active():
                draw_countdown_overlay(int(game.get_countdown_remaining()))
            else:
                draw_rectangle_gradient_ex(
                    Rectangle(0, 0, settings.board_width, settings.board_height),
                    *settings.boardBackgroundColors,
                )

            draw_word_path(game)
            game.update()

            if new_game_button.contains():
                new_game_button.color = settings.button_hover_color
            else:
                new_game_button.color = settings.button_default_color

            if new_game_button.contains() and is_mouse_button_pressed(0):
                game.start_new_board()
                time.sleep(0.2)

            if seed_button.contains() and game.seed and game.is_seed_button_ready():
                seed_button.color = settings.button_hover_color
                if is_mouse_button_pressed(0):
                    pyperclip.copy(game.seed)
                    game.seed_lockout_time = time.time() + 1
                    seed_button.color = settings.button_active_color
            elif game.is_seed_button_ready():
                seed_button.color = settings.button_default_color

            if game.is_countdown_active():
                countdown_seconds = int(game.get_countdown_remaining())
                timer_button.label = f"00:{countdown_seconds:02d}"
                timer_button.color = YELLOW
            else:
                remaining = int(game.get_time_remaining())
                timer_button.label = f"{remaining // 60:02d}:{remaining % 60:02d}"
                timer_button.color = settings.button_default_color
                if remaining <= 0:
                    timer_button.color = settings.warning_color

            new_game_button.draw()
            timer_button.draw()
            seed_button.draw()

            if game.current_word and is_mouse_button_down(0):
                draw_rectangle_rounded(current_word_box_bounds, 0.35, 10, LIGHTGRAY)
                draw_text_ex(
                    guessesFont,
                    f"Current:\n{game.current_word}",
                    Vector2(current_word_box_bounds.x + 12, current_word_box_bounds.y + 12),
                    guessesFontSize,
                    1,
                    BLACK,
                )

            draw_guess_list(game, current_word_box_bounds.y + current_word_box_bounds.height + 20)
            draw_board_grid()
            draw_board_letters(game)
            draw_invalid_message(game, current_word_box_bounds)

        end_drawing()


if __name__ == "__main__":
    main()
