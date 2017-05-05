from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *
from block import *


class Level(InstructionGroup):
    def __init__(self, text_file):
        super(Level, self).__init__()

        self.translator = Translate()
        self.add(self.translator)

        # self.jump_times = None
        # self.duck_times = None
        # self.platforms = None
        self.blocks = []
        for i in xrange(50):
            xr = PIXEL*i
            xg = PIXEL*i+PIXEL*50
            xb = PIXEL*i+PIXEL*16
            xl = PIXEL*16*i+PIXEL*16
            xh = PIXEL*16*i+PIXEL*24
            # platforms
            self.block = Block(xr, PIXEL, RED_IDX, self.translator)
            self.add(self.block)
            self.blocks.append(self.block)
            self.block = Block(xg, PIXEL, GREEN_IDX, self.translator)
            self.add(self.block)
            self.blocks.append(self.block)
            self.block = Block(xb, 3*PIXEL, BLUE_IDX, self.translator)
            self.add(self.block)
            self.blocks.append(self.block)

            # dodge blocks
            self.block = Block(xl, 2*PIXEL, WHITE_IDX, self.translator)
            self.add(self.block)
            self.blocks.append(self.block)
            self.block = Block(xh, 4*PIXEL, WHITE_IDX, self.translator)
            self.add(self.block)
            self.blocks.append(self.block)

        self.block = Block(17*PIXEL, 4*PIXEL, WHITE_IDX, self.translator, moving=True)
        self.add(self.block)
        self.blocks.append(self.block)

        self.direction = 0
        self.alive = True

    def get_current_blocks(self):
        current_blocks = []
        for b in self.blocks:
            b_pos = b.get_current_pos()
            if b_pos+b.width >= PLAYER_X and b_pos <= PLAYER_X+PLAYER_W:
                current_blocks.append(b)
        return current_blocks

    def reverse(self):
        if self.alive:
            self.direction = -1

    def forward(self):
        if self.alive:
            self.direction = 1

    def lose(self):
        self.direction = 0
        self.alive = False

    def reset(self):
        self.translator.x = 0
        self.direction = 0
        self.alive = True

    def start(self):
        self.direction = 1

    def on_update(self, dt):
        self.translator.x -= self.direction * SPEED
        if self.alive:
            self.block.on_update()
