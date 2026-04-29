from pyray import *
import random
import time

#sizing parameter for the window
window_height = 800
window_width = 1000

# sizing parameters for the boggle board, grid lines, and letter offsets
board_height = 800
board_width = 800
partitioned_fifths = (board_height / 5)
x_letter_offset = board_height / 16
y_letter_offset = board_height / 20

# initialize window size NOT board size
init_window(window_width, window_height, "Boggle")

# load font
font = load_font_ex("Arena.ttf", 100, None, 250)

# refresh button bounds
refresh_button_x = window_width - (window_width / 7)
refresh_button_y = (board_height / 16)
refresh_button_width = board_width - (board_width - 100)
refresh_button_height = board_height - (board_height - 50)
btnBounds = [refresh_button_x, refresh_button_y, 
             refresh_button_width, refresh_button_height]

# --- generate board ONCE ---
dice = {
        0 : ['F', 'R', 'Y', 'S', 'P', 'I'],
        1 : ['A', 'A', 'F', 'S', 'I', 'R'],
        2 : ['H', 'O', 'H', 'D', 'L', 'N'],
        3 : ['E', 'E', 'E', 'A', 'E', 'A'],
        4 : ['E', 'T', 'C', 'S', 'C', 'N'],
        5 : ['M', 'E', 'O', 'T', 'T', 'T'],
        6 : ['T', 'O', 'O', 'O', 'T', 'U'],
        7 : ['N', 'N', 'N', 'A', 'D', 'E'],
        8 : ['E', 'E', 'E', 'E', 'A', 'M'],
        9 : ['N', 'D', 'D', 'T', 'O', 'H'],
        10 : ['C', 'P', 'I', 'E', 'S', 'T'],
        11 : ['O', 'O', 'U', 'W', 'T', 'N'],
        12 : ['TH', 'IN', 'QU', 'HE', 'AN', 'ER'],
        13 : ['U', 'E', 'N', 'S', 'S', 'S'],
        14 : ['O', 'R', 'D', 'H', 'N', 'L'],
        15 : ['N', 'M', 'N', 'A', 'E', 'G'],
        16 : ['Z', 'B', 'QU', 'J', 'X', 'K'],
        17 : ['S', 'A', 'Y', 'F', 'R', 'I'],
        18 : ['A', 'A', 'F', 'A', 'R', 'A'],
        19 : ['P', 'W', 'R', 'G', 'V', 'R'],
        20 : ['T', 'I', 'T', 'I', 'I', 'E'],
        21 : ['P', 'E', 'L', 'C', 'T', 'I'],
        22 : ['D', 'H', 'O', 'R', 'L', 'H'],
        23 : ['E', 'U', 'A', 'G', 'M', 'E'],
        24 : ['C', 'T', 'I', 'L', 'I', 'E'],
        # 25 : ['K', 'I', 'QU', 'W', 'L', 'U'] # no implementation for adding extra die yet, MUST be commented out
    }

# randomize function: scrambles arrays of letters
def randomize_board():
    items_list = list(dice.items())
    random.shuffle(items_list)
    shuffled_dict = dict(items_list)
    
    # declare empty output list
    output = []
    
    # loop thru dict and rand 1/6 chance of a letter in val array
    for key, value in shuffled_dict.items():
        output.append(value[random.randint(0, 5)])
    return output
output = randomize_board()

# --- main loop ---
btnClicked = False
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    
    # FIXME: button checking for left click on hitbox
    btnClicked = False
    if (check_collision_point_rec(get_mouse_position(), 
        btnBounds)):
        if is_mouse_button_pressed(0):
            btnClicked = True
            output = randomize_board()
            time.sleep(0.2) # debounce
    
    # button text and rectangle drawing
    # FIXME: button does not change colors
    draw_rectangle_rec(btnBounds, GREEN if btnClicked else LIGHTGRAY)
    draw_text_ex(font, "Refresh", (btnBounds[0] + btnBounds[2] / 2 - 50, 
                                   btnBounds[1] + btnBounds[3] / 2 - 25), 20, 1, BLACK)
    # draw grid lines
    #@ FIXME: MAKE BOX AROUND LINES AND LINES DO NOT GO TO THE EDGE
    for x in range(5):
        draw_line(int(x*partitioned_fifths + partitioned_fifths), 0,
                  int(x*partitioned_fifths + partitioned_fifths), board_height, BLACK)
    for x in range(5):
        draw_line(0, int(x*partitioned_fifths + partitioned_fifths),
                  board_width, int(x*partitioned_fifths + partitioned_fifths), BLACK)

    # draw letters (DON'T pop!)
    i = 0
    for x in range(5):
        for y in range(5):
            if len(output[i]) > 1:
                pos = Vector2(
                    int(x*partitioned_fifths + x_letter_offset/2.1),
                    int(y*partitioned_fifths + y_letter_offset)
                )
            else:
                pos = Vector2(
                    int(x*partitioned_fifths + x_letter_offset),
                    int(y*partitioned_fifths + y_letter_offset)
                )
            draw_text_ex(font, output[i], pos, 100, 0, BLACK)
            i += 1
    
    end_drawing()