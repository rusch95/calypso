from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *

class Barline(InstructionGroup):
    def __init__(self, init_pos, translator):
        super(Barline, self).__init__()

        # Store parameters
        self.init_pos = init_pos
        self.x = init_pos + BAR_OFFSET
        self.translator = translator
        self.color = GREY
        
        # Create bar
        self.add(self.color)
        self.block = Rectangle(pos=(self.x, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self):
        pass
