from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *

class CheckPoint(InstructionGroup):
    def __init__(self, init_pos, translator):
        super(CheckPoint, self).__init__()

        # Store parameters
        self.init_pos = init_pos
        self.x = init_pos + BAR_OFFSET
        self.translator = translator
        self.color = LIGHT_PURPLE
        
        # Create bar
        self.add(self.color)
        self.block = Rectangle(pos=(self.x, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def set_checkpoint(self):
        self.color = PURPLE
        self.add(self.color)
        self.remove(self.block)
        self.block = Rectangle(pos=(self.x, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def unset_checkpoint(self):
        self.color = LIGHT_PURPLE
        self.add(self.color)
        self.remove(self.block)
        self.block = Rectangle(pos=(self.x, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def on_update(self):
        pass
