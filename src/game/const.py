from kivy.graphics import Color
# Constants!

# Colors
RED = Color(1,0,0)
GREEN = Color(0,1,0)
BLUE = Color(0,0,1)
WHITE = Color(1,1,1)
GREY = Color(.5,.5,.5)
GRAY = GREY
COLORS = [RED, GREEN, BLUE, WHITE]
COLORS_2 = [(1,0,0),(0,1,0),(0,0,1)]

RED_IDX = 0
GREEN_IDX = 1
BLUE_IDX = 2

WINDOW_SIZE = (1024, 768)

# Controls
START = 7
SELECT = 6

X_AXIS = 0 
Y_AXIS = 1
JOYSTICK_THRESH = 20000

FLOOR = 100

# Player Dimensions
PLAYER_X = 300
PLAYER_Y = FLOOR
PLAYER_W = 50
PLAYER_H = 150
PLAYER_DUCK_H = 50

# Block Dimensions
BLOCK_W = 50
BLOCK_H = 50

# Soon Obsolete Constants
JUMP_BOX_W = 50
JUMP_BOX_H = 50
JUMP_BOX_Y = FLOOR

DUCK_BOX_W = 50
DUCK_BOX_H = 50
DUCK_BOX_Y = FLOOR + 100

BAR_W = PLAYER_W
BAR_H = WINDOW_SIZE[1]#-FLOOR
BAR_Y = 0 #FLOOR

V_M_BOX_W = 50
V_M_BOX_H = 50
V_M_BOX_Y_MIN = FLOOR
V_M_BOX_Y_MAX = 600
V_M_BOX_SPEED = 5

PLATFORM_H = 50

SPEED = 4
SPACING = SPEED * 60





