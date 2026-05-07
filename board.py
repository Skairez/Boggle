from pyray import *
import random
import time
from raylib import GetColor, TextFormat

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
# - [DONE] add validate logic that allows only letters to connect to adjacent letters
# - [DONE]: rn any click will add a word, but should specify that the click must contain 1 letter/bound
# - [DONE]: "new game" will still countdown the main timer while the board countdown is happening


# DESIGN:
# - hover on word and see how it got made show the lines (daniel task)
# - connect letters with lines maybe animate (daniel task)
# - [DONE] add a cover for the 5 second grade period then "READY? START" reveal
#   #   # FIXME: maybe change colors for coluntdown or board BG, optional
# FIXME: adding new hitbox "die face" underneath letters, fix hitboxes instead of circles
#        use the die as a hitbox, maybe check collision polygon and insert draw_rectangle_rounded


# game variables for word bank of the player
roundTime = 180 # 180 -> 3 min round timer
roundCountdownTime = 6 # 5 second countdown before board is shown (put 6 for 5)
word = ""
already_used_letter = []
wordsGuessed = []

# colors
dieColor = GetColor(0xF7EED2ff)
countdownBackgroundColors = (PINK, YELLOW, WHITE, DARKBLUE)
boardBackgroundColors = (GetColor(0x44519Cff), GetColor(0x187F8Bff),
                         GetColor(0x060914ff), GetColor(0x187F8Bff))

#sizing parameter for the window
window_width = 1000
window_height = int(window_width * 0.8)


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
newGameFontSize = int(board_height * 0.035)
timerFontSize = int(board_height * 0.05)
guessesFontSize = int(board_height * 0.03)
countdownFontSize = int(board_height * 0.25)
boardFont = load_font_ex("PlatNomor.ttf", boggleFontSize, None, 95)
newGameFont = load_font_ex("PlatNomor.ttf", newGameFontSize, None, 95)
timerFont = load_font_ex("PlatNomor.ttf", timerFontSize, None, 95)
guessesFont = load_font_ex("PlatNomor.ttf", guessesFontSize, None, 95)
countdownFont = load_font_ex("PlatNomor.ttf", countdownFontSize, None, 95)


# FIXME: these buttons can be simplified into a class for size, only Y level changing
# refresh button default variables
refresh_button_x = int(board_width + ((window_width - board_width) * 0.2))
refresh_button_y = int(board_height / 16)
refresh_button_width = int((window_width - board_width ) * 0.6)
refresh_button_height = int(board_height * 0.1)
newBoardButtonBounds = [refresh_button_x, refresh_button_y, 
             refresh_button_width, refresh_button_height]
newBoardButtonClicked = False
newBoardButtonColor = LIGHTGRAY

# timer default variables
timer_x =  int(board_width + ((window_width - board_width) * 0.2))
timer_y = int((board_height / 16) + 100)
timer_width = int((window_width - board_width ) * 0.6)
timer_height = int(board_height * 0.1)
timerBounds = [timer_x, timer_y, timer_width, timer_height]
countdownTimer = time.time() + roundCountdownTime # countdown before round begins
threeMinuteTimer = countdownTimer + roundTime # active round time
timerButtonColor = YELLOW


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

def get_grid_coords():
    for x in range(5):
        for y in range(5):
            pos_x = int(x*partitioned_fifths + (partitioned_fifths * 0.5))
            pos_y = int(y*partitioned_fifths + (y_letter_offset * 0.8) + (board_height * 0.2) / 3.56)
            if check_collision_point_circle(get_mouse_position(), (pos_x, pos_y), 55):
                return (x, y)
    return None

# returns letter at position of mouse, if within hitbox of a letter, else returns empty string
def get_letter_at_position():
    coords = get_grid_coords()
    if coords is not None:
        x, y = coords
        return output[x * 5 + y]
    return ""

# returns grid coordinates of letter at mouse position, if within hitbox of a letter
# else returns None

# FIXME: this is uh.... yeah lol
def get_cords():
    return get_grid_coords()

lastKnownPosition = None

# --- main loop ---
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    # lowk this was meant to cover the board but i kinda fw it
    draw_rectangle_gradient_ex(Rectangle(0, 0, board_width, board_height), 
                                   boardBackgroundColors[0], boardBackgroundColors[1],
                                   boardBackgroundColors[2], boardBackgroundColors[3]) 

    # click and drag to combine letters into word, release to submit word
    # selection now uses grid coordinates for adjacency checks instead of pixel offsets
    if is_mouse_button_down(0):
        cord = get_cords()
        if cord and cord not in already_used_letter:
            if not lastKnownPosition:  # If this is the first letter being selected
                letter = get_letter_at_position()
                word = word + letter
                already_used_letter.append(cord)
                lastKnownPosition = cord
            else:
                if abs(cord[0] - lastKnownPosition[0]) <= 1 and abs(cord[1] - lastKnownPosition[1]) <= 1:  # Check if the current position is adjacent to the last known position
                    letter = get_letter_at_position()
                    word = word + letter
                    already_used_letter.append(cord)
                    lastKnownPosition = cord
    if is_mouse_button_released(0) and word != "":
        wordsGuessed.append(word)
        word = ""
        already_used_letter.clear()
        lastKnownPosition = ()

    # continuously displays list of submitted words
    for i, w in enumerate(wordsGuessed):
        draw_text_ex(guessesFont, f"{i}. {w}", 
                     Vector2(refresh_button_x, (refresh_button_y + (board_height * 0.3)) + (i * (guessesFontSize))), 
                     guessesFontSize, 1, BLACK)
    
    
    # refresh button checking for hover of mouse to turn green
    newBoardButtonClicked = False
    if (check_collision_point_rec(get_mouse_position(), newBoardButtonBounds)):
        # will highlight button green indicating mouse is within hitbox
        newBoardButtonColor = GREEN
        if is_mouse_button_pressed(0):
            newBoardButtonClicked = True
            output = randomize_board()
            # idk i just add countdown into 3m timer cause it dont work otherwise lul
            threeMinuteTimer = time.time() + roundTime + roundCountdownTime # 186 sec- add 5 sec grace
            countdownTimer = time.time() + roundCountdownTime
            time.sleep(0.2) # debounce
            wordsGuessed = []    
    else:
        newBoardButtonColor = LIGHTGRAY
    
    # draw buttons and timer
    draw_rectangle_rounded(newBoardButtonBounds, .5, 10, newBoardButtonColor)
    draw_rectangle_rounded(timerBounds, .5, 10, timerButtonColor)


    # draw refresh button
    # FIXME: magic numbers
    draw_text_ex(newGameFont, "New Game", 
                Vector2(int(newBoardButtonBounds[0] + (newBoardButtonBounds[2] * 0.5) - (board_width * newGameFontSize * 0.0025)), 
                        int(newBoardButtonBounds[1] + (newBoardButtonBounds[3] * 0.4))), 
                newGameFontSize, 1, BLACK)
    
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
            if output[i] == "IN":
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.35)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            elif len(output[i]) > 1:
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.52)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            elif output[i] == "I":
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.11)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            else:
                pos = Vector2(
                    int(x*partitioned_fifths + (partitioned_fifths * 0.5) - (boggleFontSize * 0.24)),
                    int(y*partitioned_fifths + (y_letter_offset * 0.8))
                )
            pos_x = int(x*partitioned_fifths + (partitioned_fifths * 0.5))
            pos_y = int(y*partitioned_fifths + (y_letter_offset * 0.8) + (board_height * 0.2) / 3.56)
            letterDieFace = (x*partitioned_fifths + (partitioned_fifths * 0.05), 
                             y*partitioned_fifths + (partitioned_fifths * 0.05), 
                             partitioned_fifths * 0.9, 
                             partitioned_fifths * 0.9)
            output_currently = output[i]
            # FIXME: not displaying under the letter :(
            draw_rectangle_rounded(letterDieFace, 0.5, 10, dieColor);
            draw_text_ex(boardFont, output[i], pos, boggleFontSize, 0, BLACK)
            # draw_circle_lines(pos_x, pos_y, 55, RED);
            position_string_dict[(pos_x, pos_y)] = output_currently
            i += 1
    
    # Timer countdown display
    # this must come last so that the board can be "hidden" during countdown
    # print(f"Countdown timer: {countdownTimer}, Current time: {time.time()}")
    if int(countdownTimer - time.time()) > 0: # FIXME: this doesnt seem to activate at all
        countdownTimerHolder = abs(int(countdownTimer - time.time()))
        countdownTimerSec = int(abs(countdownTimerHolder % 60))
        draw_text_ex(timerFont, f"00:{countdownTimerSec:02d}", 
                    Vector2(int(timerBounds[0] + (timerBounds[2] * timerFontSize * 0.0025)), 
                            int(timerBounds[1] + (timerBounds[3] * 0.3))), 
                    timerFontSize, 1, BLACK)
        timerButtonColor = YELLOW
        # FIXME: play around with colors so its diff than the playing board background
        draw_rectangle_gradient_ex(Rectangle(0, 0, board_width, board_height), 
                                   PINK, YELLOW, WHITE, DARKBLUE)
        # FIXME: center and enlarge countdown text
        if countdownTimerSec > 3:
            draw_text_ex(countdownFont, "Ready?",
                        Vector2(int(board_width * 0.15), 
                        int(board_height / 2 - (countdownFontSize * 0.5))),
                        countdownFontSize, 1, BLACK)
        elif countdownTimerSec <= 3 and countdownTimerSec > 1:
            draw_text_ex(countdownFont, "Set...",
                        Vector2(int(board_width * 0.3), 
                        int(board_height / 2 - (countdownFontSize * 0.5))),
                        countdownFontSize, 1, BLACK)
        elif countdownTimerSec <= 1:
            draw_text_ex(countdownFont, "Go!",
                        Vector2(int(board_width * 0.35), 
                        int(board_height / 2 - (countdownFontSize * 0.5))),
                        countdownFontSize, 1, BLACK)
    else:
        timerButtonColor = LIGHTGRAY
        timerValue = int(threeMinuteTimer - time.time())
        # print(f"Timer value: {timerValue}, Three-minute timer: {threeMinuteTimer}")
        timerMin = int(abs(timerValue)) // 60
        timerSec = int(abs(timerValue)) % 60
        timerText = f"{timerMin:02d}:{timerSec:02d}"
        draw_text_ex(timerFont, timerText,
                    Vector2(int(timerBounds[0] + (timerBounds[2] * timerFontSize * 0.0025)), 
                            int(timerBounds[1] + (timerBounds[3] * 0.3))),
                    timerFontSize, 1, BLACK)
        # if timer = 0, timer flashes between red and grey
        if timerValue <= 0 and (abs(timerValue) // 1) % 2 == 0: # first red lasts 2 seconds?, then 1 sec alt
            draw_rectangle_rec(timerBounds, RED)
            draw_text_ex(timerFont, "00:00",
                    Vector2(int(timerBounds[0] + (timerBounds[2] * timerFontSize * 0.0025)), 
                            int(timerBounds[1] + (timerBounds[3] * 0.3))),
                    timerFontSize, 1, WHITE)
            timerFlash = True
        elif timerValue <= 0 and (abs(timerValue) // 1) % 2 != 0:
            draw_rectangle_rec(timerBounds, GRAY)
            draw_text_ex(timerFont, "00:00",
                    Vector2(int(timerBounds[0] + (timerBounds[2] * timerFontSize * 0.0025)), 
                            int(timerBounds[1] + (timerBounds[3] * 0.3))),
                    timerFontSize, 1, WHITE)
        
    
    # draw_rectangle_rounded((0, 0, board_width, board_height), 0.5, 10, WHITE);

    
    end_drawing()