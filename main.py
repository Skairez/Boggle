from pyray import *
import random
import time

window_height = 800
window_width = 800
partitioned_fifths = (window_height / 5)

init_window(window_height, window_width, "Boggle Playfield")

while not window_should_close():
    begin_drawing()

    clear_background(WHITE)
    
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
    # declare empty output list
    output = []

    # list to shuffle back to dict
    items_list = list(dice.items())
    random.shuffle(items_list)
    shuffled_dict = dict(items_list)

    # loop thru dict and rand 1/6 chance of a letter in val array
    for key, value in shuffled_dict.items():
        output.append(value[random.randint(0, 5)])
        
    # draw vert lines every 200 pixels DrawLine(int startPosX, int startPosY, int endPosX, int endPosY, Color color);
    # loop
    for x in range(5):
        draw_line(int (x*partitioned_fifths + partitioned_fifths), 0, int (x*partitioned_fifths + partitioned_fifths), window_height, BLACK)
    for x in range(5):
        draw_line(0, int (x*partitioned_fifths + partitioned_fifths), window_width, int (x*partitioned_fifths + partitioned_fifths), BLACK)
    
    for x in range(5):
        for y in range(5):
            # fix 50 and 40 to be scalable to any size not sure the formula yet
            # 100 is font size
            draw_text(output.pop(), int (x*partitioned_fifths+50), int (y*partitioned_fifths+40), 100, BLACK)  

    time.sleep(5)
    
    end_drawing()
close_window()

