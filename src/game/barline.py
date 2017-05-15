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
        self.block = Rectangle(pos=(self.x-22, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def highlight(self):
        self.remove(self.block)
        self.block = Rectangle(pos=(self.x-22, 0), size=(BAR_W, BAR_H))
        self.add(WHITE)
        self.add(self.block)
        self.add(self.color)

    def un_highlight(self):
        self.remove(self.block)
        self.block = Rectangle(pos=(self.x-22, 0), size=(BAR_W, BAR_H))
        self.add(self.block)

    def on_update(self):
        pass
