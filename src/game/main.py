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
from block import *

import pdb

Window.size = WINDOW_SIZE

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.info = topleft_label()
        self.add_widget(self.info)

        self.canvas.add(Color(.4, .4, .75))
        self.canvas.add(Rectangle(pos=(0,0),size=Window.size))

        self.player = Player((PLAYER_X, PLAYER_Y))
        self.canvas.add(self.player)

        self.level = Level('level.txt')
        self.canvas.add(self.level)

        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Window.bind(on_joy_hat=self.on_joy_hat)
        self.audio = MidiController("music/grieg_mountain_king.mid", self.level.on_update)
      
    def on_key_down(self, keycode, modifiers):
        if keycode[1] == 'up':
            self.up()

        if keycode[1] == 'down':
            self.down()

        color_idx = lookup(keycode[1], 'asd', (RED_IDX, GREEN_IDX, BLUE_IDX))
        if color_idx != None:
            self.set_color(color_idx)

        if keycode[1] == 'left':
            self.left()

        if keycode[1] == 'right':
            self.right()

        if keycode[1] == 'p':
            self.start()

        if keycode[1] == 'r':
            self.reset()

    def on_key_up(self, keycode):
        if self.level.alive:
            if keycode[1] == 'down':
                self.neutral()

    def on_joy_button_down(self, window, null, button):
        if button == START:
            self.start()

        if button == SELECT:
            self.reset()

        mapping = {0: GREEN_IDX, 1: RED_IDX, 2: BLUE_IDX}
        if button in mapping:
            color = mapping[button]
            self.set_color(color)

    def on_joy_axis(self, win, stickid, axisid, value):
        if axisid == X_AXIS and value < -JOYSTICK_THRESH:
            self.left()
        if axisid == X_AXIS and value > JOYSTICK_THRESH:
            self.right()
        if axisid == Y_AXIS and value < -JOYSTICK_THRESH:
            self.up()
        if axisid == Y_AXIS and value > JOYSTICK_THRESH:
            self.down()
        if axisid == Y_AXIS and -JOYSTICK_THRESH < value < JOYSTICK_THRESH:
            self.neutral()

    def on_joy_hat(self, window, null1,  null2, coords):
        x, y = coords
        if y == 1:
            self.up()
        if y == -1:
            self.down()
        if coords == (0, 0):
            self.neutral()
        if x == 1:
            self.right()
        if x == -1:
            self.left()

    def up(self):
        if self.level.alive:
            self.player.jump()

    def down(self):
        if self.level.alive:
            self.player.duck()

    def neutral(self):
        if self.level.alive:
            self.player.un_duck()

    def left(self):
        if self.level.alive and self.level.direction == 1:
            def complete_reverse():
                self.level.reverse()
                self.player.left()
            self.audio.reverse(complete_reverse)

    def right(self):
        if self.level.alive and self.level.direction == -1:
            def complete_reverse():
                self.level.forward()
                self.player.right()
            self.audio.reverse(complete_reverse)

    def start(self):
        if self.level.alive:
            self.level.start()
            self.audio.start()

    def reset(self):
        self.player.un_duck()
        y_pos,color_idx,y_vel = self.level.reset()
        self.player.reset(y_pos,color_idx,y_vel)
        self.audio.reset()

    def set_color(self, color_idx):
        if self.level.alive:
            self.player.set_color(color_idx)


    def lose(self):
        # pass
        self.level.lose()
        self.audio.reset()

    # checks for loss conditions and returns ground level if player is on ground, otherwise
    def check_block_collision_and_death(self):
        # did you fall off?
        if self.player.pos[1] < 0:
            self.lose()

        current_blocks = self.level.get_current_blocks()
        # fall if no blocks
        if not current_blocks:
            return 0
        
        for b in current_blocks:
            ground = b.on_ground(self.player)
            # check if on the ground and return ground level if so
            if ground:
                return ground
            # check if a collision has occured
            possible_loss = b.check_game_loss(self.player)
            if possible_loss:
                self.lose()

        return 0

    def on_update(self):
        dt = 1
        self.info.text = 'fps:%d' % kivyClock.get_fps()
        ground = self.check_block_collision_and_death()
        self.player.on_update(dt, self.level.alive, ground)
        self.level.check_checkpoint(self.player.pos[1], self.player.color_idx, self.player.y_vel)
        self.level.on_update(dt)
        self.audio.on_update()

run(MainWidget)
