from raylib import GetColor
from pyray import PINK, YELLOW, WHITE, DARKBLUE, LIGHTGRAY, GREEN, BEIGE, BLACK, RED, GRAY

window_width = 1000
window_height = int(window_width * 0.8)
board_width = int(window_width * 0.8)
board_height = window_height
partitioned_fifths = board_height / 5
x_letter_offset = int(board_width * 0.2)
y_letter_offset = int(board_height * 0.05)

roundTime = 180
roundCountdownTime = 6
INVALID_MESSAGE_DURATION = 2.5

# panel button layout
button_x = int(board_width + ((window_width - board_width) * 0.2))
button_width = int((window_width - board_width) * 0.6)
button_height = int(board_height * 0.1)
button_spacing = int(board_height * 0.12)

# colors
dieColor = GetColor(0xF7EED2ff)
selected_die_color = GetColor(0xF0D56Cff)
countdownBackgroundColors = (PINK, YELLOW, WHITE, DARKBLUE)
boardBackgroundColors = (
    GetColor(0x44519Cff),
    GetColor(0x187F8Bff),
    GetColor(0x060914ff),
    GetColor(0x187F8Bff),
)

# generic UI colors
button_default_color = LIGHTGRAY
button_hover_color = GREEN
button_active_color = BEIGE
text_color = BLACK
warning_color = RED
expired_color = GRAY
