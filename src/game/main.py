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
import globals
from const import *
from block import *

import pdb

Window.size = WINDOW_SIZE


class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()


        import sys
        try:
            start_spot = int(sys.argv[2])
        except:
            start_spot = 0

        self.info = topleft_label()
        self.add_widget(self.info)

        background = Image(source='../../data/background/city2.png').texture
        self.background_color = BACKGROUND
        self.canvas.add(self.background_color)
        self.canvas.add(Rectangle(pos=(0, 0), 
                        size=Window.size, 
                        texture=background))

        self.background_texture = None

        self.audio = MidiController("music/grieg_mountain_king_with_levels.mid", self.level_on_update, start_spot=start_spot)
        self.level = Level(self.audio.platform_messages)
        self.player = Player((PLAYER_X, PLAYER_Y), self.level)
        
        self.canvas.add(self.level)

        # create reverse translator to have player in the right place
        self.reverse_translator = Translate()
        self.canvas.add(self.reverse_translator)
        self.canvas.add(self.player)

        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Window.bind(on_joy_hat=self.on_joy_hat)

        self.desaturate = False
        self.time = 0

        #Hack to setup correct initiall color
        self.set_color(0)
        


    def level_on_update(self, *args, **kwargs):
        return self.level.on_update(*args, **kwargs)

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

    def on_joy_hat(self, window, null1, null2, coords):
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
            self.level.set_next_barline()
            
            def complete_reverse(*args, **kwargs):
                self.level.reverse(*args, **kwargs)
                self.player.left()

            self.audio.reverse(complete_reverse)

    def right(self):
        if self.level.alive and self.level.direction == -1:
            self.level.set_previous_barline()

            def complete_reverse(*args, **kwargs):
                self.level.forward(*args, **kwargs)
                self.player.right()

            self.audio.reverse(complete_reverse)

    def start(self):
        if self.level.alive:
            self.level.start()
            self.audio.start()

    def reset(self):
        self.player.un_duck()
        y_pos, color_idx, y_vel = self.level.reset()
        self.player.reset(y_pos, color_idx, y_vel)
        self.audio.reset(lost=False)

        self.desaturate = False
        self.set_color(0)

    def set_color(self, color_idx):
        if self.level.alive:
            self.player.set_color(color_idx)

        if color_idx == 0:
            RED.rgb = COLOR_VALS[0]
            GREEN.rgb = DESAT_VALS[1]
            BLUE.rgb = DESAT_VALS[2]
            BACKGROUND.rgb = BACKGROUND_VALS[0]
        elif color_idx == 1:
            RED.rgb = DESAT_VALS[0]
            GREEN.rgb = COLOR_VALS[1]
            BACKGROUND.rgb = BACKGROUND_VALS[1]
        else:
            RED.rgb = DESAT_VALS[0]
            GREEN.rgb = DESAT_VALS[1]
            BLUE.rgb = COLOR_VALS[2]
            BACKGROUND.rgb = BACKGROUND_VALS[2]

        
    def lose(self):
        self.desaturate = True
        self.level.lose()
        self.audio.reset(lost=True)


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
        prev_time = self.time
        new_time = self.audio.sched.get_tick() * (512. / 480.)
        dt = int((new_time * 1. - prev_time) / 16)
        self.time = prev_time + dt * 16

        self.info.text = 'fps:%d' % kivyClock.get_fps()
        ground = self.check_block_collision_and_death()
        self.player.on_update(dt, self.level.alive, ground)
        self.level.check_checkpoint(self.player.pos[1], self.player.color_idx, self.player.y_vel)
        self.audio.on_update()

        if self.desaturate:
            for color in CYCLE_COLORS:
                if color.s > .05:
                    color.s -= .05

        # update reverse translator
        self.reverse_translator.x = -self.level.translator.x

run(MainWidget)
