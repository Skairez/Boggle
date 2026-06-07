# FIXME: these buttons can be simplified into a class for size, only Y level changing
# refresh button default variables
class Button:
    button_x = int(board_width + ((window_width - board_width) * 0.2))
    button_y = int(board_height / 16) # this must be adjustable for mult
    button_width = int((window_width - board_width ) * 0.6)
    button_height = int(board_height * 0.1)
    buttonBounds = [button_x, button_y, 
                button_width, button_height]
    ButtonClicked = False
