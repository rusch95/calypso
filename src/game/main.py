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
from audio_controller import *
from const import *

import pdb

Window.size = (1024, 768)

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.player = Player((PLAYERX, PLAYERY))
        self.canvas.add(self.player)

        self.level = Level('level.txt')
        self.canvas.add(self.level)
        # self.audio_ctrl = AudioController("mountain_king.wav")

        self.info = topleft_label()
        self.add_widget(self.info)
      
    def on_key_down(self, keycode, modifiers):
        if self.level.alive:
            if keycode[1] == 'up':
                self.player.jump()

            if keycode[1] == 'down':
                self.player.duck()

            color_idx = lookup(keycode[1], 'asd', (1,2,3))
            if color_idx:
                self.player.set_color(color_idx-1)

            if keycode[1] == 'left':
                self.level.reverse()

            if keycode[1] == 'right':
                self.level.forward()

        if keycode[1] == 'r':
            self.level.reset()
            self.player.reset()
            # self.audio_ctrl.restart()

    def on_key_up(self, keycode):
        if self.level.alive:
            if keycode[1] == 'down':
                self.player.un_duck()

    def check_color_loss(self):
        platform = self.level.get_current_platform()
        if platform == None:
            self.level.lose()
            return
        platform_color = platform.color.rgb
        person_color = self.player.color.rgb
        if platform_color != person_color and not self.level.is_between_platforms():
            self.level.lose()

    def check_block_loss(self):
        if self.level.is_current_duck():
            pos = self.player.pos[1]
            height = self.player.size[1]
            if pos + height > DUCKBOXY:
                self.level.lose()
        elif self.level.is_current_jump():
            pos = self.player.pos[1]
            if pos < JUMPBOXY + JUMPBOXH:
                self.level.lose()
                # self.audio_ctrl.stop()

    def on_update(self):
        dt = 1
        self.info.text = 'fps:%d' % kivyClock.get_fps()
        self.player.on_update(dt)
        self.level.on_update(dt)
        self.check_color_loss()
        self.check_block_loss()
        # self.audio_ctrl.on_update()

run(MainWidget)
