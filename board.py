from pyray import *
import random
import time
from raylib import TextFormat

## TO DO

# REFACTOR:
# - make button class to easily duplicate button sizes
# - add file for game parameter? (eg. timer length)

# LOGIC:
# - make text input option
# - lock board until "start" is clicked and after timer runs out
# - add way to delete last word submitted, potentially add "pages" of submitted words (for genius players)
# - create 4 letter word limit
# - score points based on word length, flag words not in dictionary and give players option to vote to accept word into dict
# - make statistics for words played
# - MULTIPLAYER

# DESIGN:
# - hover on word and see how it got made show the lines
# - connect letters with lines maybe animate
# - add a cover for the 5 second grade period then "READY? START" reveal


# game variables for word bank of the player
roundTime = 186 # 3 min + 5 sec grace
word = ""
already_used_letter = []
wordsGuessed = []


#sizing parameter for the window
window_height = 800
window_width = 1000

# sizing parameters for the boggle board, grid lines, and letter offsets
board_height = window_height
board_width = int(window_width * 0.8)
partitioned_fifths = (board_height / 5)
x_letter_offset = int(board_width * 0.2)
y_letter_offset = int(board_height * 0.05)


# initialize window size NOT board size
init_window(window_width, window_height, "Boggle")


# Load font with specific characters (0-9, A-Z, a-z)
boggleFontSize = int(board_height * 0.15)
char_codes = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))  # digits, uppercase, lowercase
font = load_font_ex("Arena.ttf", boggleFontSize, None, 95)
numFont = load_font_ex("Arena.ttf", 32, None, 95)


# FIXME: these buttons can be simplified into a class for size, only Y level changing
# refresh button default variables
refresh_button_x = int(board_width + ((window_width - board_width) * 0.2))
refresh_button_y = int(board_height / 16)
refresh_button_width = int((window_width - board_width ) * 0.6)
refresh_button_height = int(board_height * 0.1)
newBoardButtonBounds = [refresh_button_x, refresh_button_y, 
             refresh_button_width, refresh_button_height]
newBoardButtonClicked = False

# timer default variables
timer_x =  int(board_width + ((window_width - board_width) * 0.2))
timer_y = int((board_height / 16) + 100)
timer_width = int((window_width - board_width ) * 0.6)
timer_height = int(board_height * 0.1)
timerBounds = [timer_x, timer_y, timer_width, timer_height]
threeMinuteTimer = time.time() + roundTime # add 5 sec grace- also much

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



position_string_dict = dict()
# returns letter at position of mouse, if within hitbox of a letter, else returns empty string
def get_letter_at_position():
        for x in range(5):
            for y in range(5):
                
                pos_x = int(x*partitioned_fifths + (partitioned_fifths * 0.5))
                pos_y = int(y*partitioned_fifths + (y_letter_offset * 0.8))
                        
                if (check_collision_point_circle(get_mouse_position(), (pos_x , pos_y + 44), 55)):
                    letter_at_pos = position_string_dict[(pos_x, pos_y + 44)]
                    return letter_at_pos
                
                else: continue  
        return ""


# returns cords of letter at position of mouse, if within hitbox of a letter, else returns empty tuple
def get_cords():
        for x in range(5):
            for y in range(5):
                
                pos_x = int(x*partitioned_fifths + (partitioned_fifths * 0.5))
                pos_y = int(y*partitioned_fifths + (y_letter_offset * 0.8))
                        
                if (check_collision_point_circle(get_mouse_position(), (pos_x, pos_y + 44), 55)):
                    cord = (pos_x, pos_y + 44)
                    return cord
                
                else: continue




# --- main loop ---

while not window_should_close():
    begin_drawing()
    clear_background(WHITE)

    # click and drag to combine letters into word, release to submit word
    if is_mouse_button_down(0):
        cord = get_cords()
        if cord and cord not in already_used_letter:
                letter = get_letter_at_position()
                word = word + letter
                already_used_letter.append(cord)

    if is_mouse_button_released(0):
        wordsGuessed.append(word)
        word = ""
        already_used_letter.clear()



    # continuously displays list of submitted words
    # FIXME: magic numbers: y offset, font size
    # FIXME: cannot list words with numbers due to default font issue
    for i, w in enumerate(wordsGuessed):
        draw_text_ex(font, f"{i} : {w}", 
                     Vector2(refresh_button_x, (refresh_button_y + (board_height * 0.3 )) + (i * 30)), 
                     30, 1, BLUE)
    
    
    
    # refresh button checking for hover of mouse to turn green
    newBoardButtonClicked = False
    if (check_collision_point_rec(get_mouse_position(), newBoardButtonBounds)):
        # will highlight button green indicating mouse is within hitbox
        newBoardButtonColor = GREEN
        if is_mouse_button_pressed(0):
            newBoardButtonClicked = True
            output = randomize_board()
            threeMinuteTimer = time.time() + roundTime # 186 sec- add 5 sec grace
            time.sleep(0.2) # debounce
            wordsGuessed = []
    else:
        newBoardButtonColor = LIGHTGRAY
    
    
    
    # draw buttons and timer
    draw_rectangle_rec(newBoardButtonBounds, newBoardButtonColor)
    draw_rectangle_rec(timerBounds, LIGHTGRAY)


    # draw refresh button
    draw_text_ex(font, "New Board", (newBoardButtonBounds[0] + (newBoardButtonBounds[2] / 2) - 45, 
                                   newBoardButtonBounds[1] + (newBoardButtonBounds[3] / 2) - 10), (board_height / 39), 1, BLACK)
    
    
    # FIXME: only displays in default font
    timerValue = int(threeMinuteTimer - time.time())
    timerMin = int(abs(timerValue)) // 60
    timerSec = int(abs(timerValue)) % 60
    timerText = f"{timerMin:02d}:{timerSec:02d}"
    # draw_text_ex(numFont, timerText,
    #             Vector2(500, 500),
    #             20, 1, BLACK)
    draw_text(timerText,
                int(timerBounds[0] + (timerBounds[2] * 0.1)), 
                int(timerBounds[1] + (timerBounds[3] * 0.25)), 
                40, BLACK)

    
    # if timer = 0, timer flashes between red and grey
    if timerValue <= 0 and (abs(timerValue) // 1) % 2 == 0: # first red lasts 2 seconds?, then 1 sec alt
        draw_rectangle_rec(timerBounds, RED)
        draw_text("00:00",
                int(timerBounds[0] + (timerBounds[2] * 0.1)), 
                int(timerBounds[1] + (timerBounds[3] * 0.25)), 
                40, WHITE)
        timerFlash = True
    elif timerValue <= 0 and (abs(timerValue) // 1) % 2 != 0:
        draw_rectangle_rec(timerBounds, GRAY)
        draw_text("00:00",
                int(timerBounds[0] + (timerBounds[2] * 0.1)), 
                int(timerBounds[1] + (timerBounds[3] * 0.25)), 
                40, WHITE)
    
    
    # boggle board grid lines
    for x in range(5):
        draw_line(int(x*partitioned_fifths + partitioned_fifths), 0,
                  int(x*partitioned_fifths + partitioned_fifths), board_height, BLACK)
    for x in range(5):
        draw_line(0, int(x*partitioned_fifths + partitioned_fifths),
                  board_width, int(x*partitioned_fifths + partitioned_fifths), BLACK)



    # draw letters for the boggle board (DON'T pop!)
    i = 0
    for x in range(5):
        for y in range(5):
            if len(output[i]) > 1:
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.55)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            elif output[i] == "I":
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.15)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            else:
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.3)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            pos_x = int(x*partitioned_fifths + (partitioned_fifths * 0.5))
            pos_y = int(y*partitioned_fifths + (y_letter_offset * 0.8))
            output_currently = output[i]
            draw_text_ex(font, output[i], pos, boggleFontSize, 0, BLACK)
            draw_circle_lines(pos_x, pos_y + 44, 55, RED);
            position_string_dict[(pos_x, pos_y + 44)] = output_currently
            i += 1
    
    end_drawing()