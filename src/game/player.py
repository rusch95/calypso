from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *

PLAYER_TEXTURES = [Image(source='../../data/dat_boi_red.png').texture,
                   Image(source='../../data/dat_boi_green.png').texture,
                   Image(source='../../data/dat_boi_blue.png').texture]

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
        self.person = Rectangle(texture=PLAYER_TEXTURES[self.color_idx], pos=self.pos, size=self.size)
        self.add(WHITE)
        self.add(self.person)
        self.dir_right = False

    def jump(self):
        if self.can_jump:
            self.y_vel = self.jump_vel
            self.can_jump = False
            self.jumped = True

    def duck(self):
        self.size = (PLAYER_W, PLAYER_DUCK_H)

    def un_duck(self):
        self.size = (PLAYER_W, PLAYER_H)

    def right(self):
        new_frame = self.person.texture
        if self.dir_right == True:
            self.dir_right = False
            new_frame.flip_horizontal()
        self.person.texture = new_frame

    def left(self):
        new_frame = self.person.texture
        if self.dir_right == False:
            self.dir_right = True
            new_frame.flip_horizontal()
        self.person.texture = new_frame

    def set_color(self, color_idx):
        self.color_idx = color_idx
        self.person.texture = PLAYER_TEXTURES[color_idx]

    def reset(self):
        self.pos = self.init_pos
        self.y_vel = 0
        self.texture = PLAYER_TEXTURES[self.color_idx]
        self.color_idx = RED_IDX

    def on_ground(self):
        return self.pos[1] == FLOOR

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
        
        # Update person
        self.person.pos = self.pos
        self.person.size = self.size
        self.jumped = False
