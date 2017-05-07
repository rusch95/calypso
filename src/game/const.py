from kivy.graphics import Color
# Constants!

# Colors
RED = Color(1,0,0)
GREEN = Color(0,1,0)
BLUE = Color(0,.4,1)
WHITE = Color(1,1,1)
GREY = Color(.5,.5,.5)
GRAY = GREY
LIGHT_PURPLE = Color(1,.75,1)
PURPLE = Color(.5,0,.5)
COLORS = [RED, GREEN, BLUE, WHITE]
COLORS_2 = [(1,0,0),(0,1,0),(0,0,1)]

RED_IDX = 0
GREEN_IDX = 1
BLUE_IDX = 2
WHITE_IDX = 3

# size of window
WINDOW_SIZE = (1024, 768)

# Controls
START = 7
SELECT = 6

X_AXIS = 0 
Y_AXIS = 1
JOYSTICK_THRESH = 20000

FLOOR = 128

# Player Dimensions

PIXEL = 64

PLAYER_X = 6*PIXEL
PLAYER_Y = 2*PIXEL
PLAYER_W = PIXEL
PLAYER_H = 2*PIXEL
PLAYER_DUCK_H = 1.33 * PIXEL

# Block Dimensions
BLOCK_W = PIXEL
BLOCK_H = PIXEL
BLOCK_SPEED = 1

# Moving Block Heights
BLOCK_MIN = 2*PIXEL
BLOCK_MAX = 10*PIXEL

# Barline Paremeters:
BAR_W = 10
BAR_H = WINDOW_SIZE[1]
BAR_OFFSET = PIXEL/2-BAR_W

# Speed of level
SPEED = 4





