import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *

from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate

from level import *
from player import *

import pdb

Window.size = (1024, 768)

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.player = Player((100,100))
        self.canvas.add(self.player)

        self.level = Level('level.txt')
        self.canvas.add(self.level)

        self.info = topleft_label()
        self.add_widget(self.info)
      
    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'up':
            self.player.jump()

        if keycode[1] == 'down':
            self.player.duck()

        color_idx = lookup(keycode[1], 'asd', (1,2,3))
        if color_idx:
            self.player.set_color(color_idx-1)

    def on_key_up(self, keycode):
        if keycode[1] == 'down':
            self.player.un_duck()

    def on_update(self):
        dt = 1
        self.info.text = 'fps:%d' % kivyClock.get_fps()
        self.player.on_update(dt)
        self.level.on_update(dt)

run(MainWidget)
