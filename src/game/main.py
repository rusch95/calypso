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
from music.midi_controller import MidiController
from const import *

import pdb

Window.size = WINDOW_SIZE

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.info = topleft_label()
        self.add_widget(self.info)

        self.player = Player((PLAYER_X, PLAYER_Y))
        self.canvas.add(self.player)

        self.level = Level('level.txt')
        self.canvas.add(self.level)

        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Window.bind(on_joy_hat=self.on_joy_hat)
        self.audio = MidiController("music/grieg_mountain_king.mid", self.level.on_update)
      
    def on_key_down(self, keycode, modifiers):
        if self.level.alive:
            if keycode[1] == 'up':
                self.player.jump()

            if keycode[1] == 'down':
                self.player.duck()

            color_idx = lookup(keycode[1], 'asd', (0,1,2))
            if color_idx:
                self.player.set_color(color_idx)

            if keycode[1] == 'left' and self.level.direction == 1:
                self.audio.reverse(self.level.reverse)

            if keycode[1] == 'right' and self.level.direction == -1:
                self.audio.reverse(self.level.forward)

            if keycode[1] == 'p':
                self.level.start()
                self.audio.start()

        if keycode[1] == 'r':
            self.level.reset()
            self.player.reset()
            self.audio.reset()

    def on_key_up(self, keycode):
        if self.level.alive:
            if keycode[1] == 'down':
                self.player.un_duck()

    def on_joy_hat(self, window, null1,  null2, coords):
        x, y = coords
        if y == 1:
            self.player.jump()
        if y == -1:
            self.player.duck()
        if coords == (0, 0):
            if self.level.alive:
                self.player.un_duck()
        if x == 1 and self.level.direction == -1:
            self.audio.reverse(self.level.forward)
        if x == -1 and self.level.direction == 1:
            self.audio.reverse(self.level.reverse)

    def on_joy_button_down(self, window, null, button):
        print null, button
        mapping = {0: 1, 1: 0, 2: 2}
        if button in mapping:
            color_idx = mapping[button]
            self.player.set_color(color_idx)

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
            if pos + height > DUCK_BOX_Y:
                self.level.lose()
                
        elif self.level.is_current_jump():
            pos = self.player.pos[1]
            if pos < JUMP_BOX_Y + JUMP_BOX_H:
                self.level.lose()

    def on_update(self):
        dt = 1
        self.info.text = 'fps:%d' % kivyClock.get_fps()
        self.player.on_update(dt)
        self.level.on_update(dt)
        self.check_color_loss()
        self.check_block_loss()
        self.audio.on_update()

run(MainWidget)
