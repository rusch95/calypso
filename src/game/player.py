from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *

class TextureHolder(object):
    def __init__(self, texture):
        self.texture = texture
        self.right = True

class Player(InstructionGroup):
    def __init__(self, init_pos):
        super(Player, self).__init__()

        # Set the physics of the person
        self.init_pos = init_pos
        self.pos = init_pos
        self.y_vel = 0
        self.can_jump = True
        self.jump_vel = 20
        self.gravity = -1
        self.jumped = False

        # Create a Person
        self.size = (PLAYER_W, PLAYER_H)
        self.color_idx = 0
        self.frame = 0

        red = Image(source='../../data/player_red.png').texture
        green = Image(source='../../data/player_green.png').texture
        blue = Image(source='../../data/player_blue.png').texture
        red_duck = Image(source='../../data/player_duck_red.png').texture
        green_duck = Image(source='../../data/player_duck_green.png').texture
        blue_duck = Image(source='../../data/player_duck_blue.png').texture
        red_frames = [TextureHolder(red.get_region(64 * x, 0, 64, 128)) for x in xrange(8)]
        green_frames = [TextureHolder(green.get_region(64 * x, 0, 64, 128)) for x in xrange(8)]
        blue_frames = [TextureHolder(blue.get_region(64 * x, 0, 64, 128)) for x in xrange(8)]
        red_duck_frames = [TextureHolder(red_duck.get_region(64 * x, 0, 64, 102)) for x in xrange(8)]
        green_duck_frames = [TextureHolder(green_duck.get_region(64 * x, 0, 64, 102)) for x in xrange(8)]
        blue_duck_frames = [TextureHolder(blue_duck.get_region(64 * x, 0, 64, 102)) for x in xrange(8)]

        self.normal_frames = [red_frames, green_frames, blue_frames]
        self.duck_frames = [red_duck_frames, green_duck_frames, blue_duck_frames]
        self.cur_frames = self.normal_frames

        self.person = Rectangle(texture=red_frames[0].texture, pos=self.pos, size=self.size)
        self.add(WHITE)
        self.add(self.person)
        self.dir_right = True

    def jump(self):
        if self.can_jump:
            self.y_vel = self.jump_vel
            self.can_jump = False
            self.jumped = True

    def duck(self):
        self.cur_frames = self.duck_frames
        self.size = (PLAYER_W, PLAYER_DUCK_H)

    def un_duck(self):
        self.cur_frames = self.normal_frames
        self.size = (PLAYER_W, PLAYER_H)

    def right(self):
        self.dir_right = True

    def left(self):
        self.dir_right = False

    def set_color(self, color_idx):
        self.color_idx = color_idx

    def reset(self):
        self.dir_right = True
        self.pos = self.init_pos
        self.y_vel = 0
        self.color_idx = RED_IDX

    def on_ground(self):
        return self.pos[1] == FLOOR

    def next_frame(self):
        self.frame += 1
        frames = self.cur_frames[self.color_idx]
        new_frame = frames[self.frame / 5 % len(frames)]
        if self.dir_right != new_frame.right:
            new_frame.right = self.dir_right
            new_frame.texture.flip_horizontal()

        self.person.texture = new_frame.texture

    def on_update(self, dt, alive, ground):
        # Update position with physics
        if alive:
            self.y_vel += dt*self.gravity
            if ground and not self.jumped:
                self.pos = (self.pos[0], ground)
            else:
                self.pos = (self.pos[0], self.pos[1] + dt * self.y_vel)
        if self.pos[1] == ground:
            self.can_jump = True
            self.y_vel = 0
        
        self.next_frame()

        # Update person
        self.person.pos = self.pos
        self.person.size = self.size
        self.jumped = False
