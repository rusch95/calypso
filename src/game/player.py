from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from colors import *
from const import *

class Player(InstructionGroup):
    def __init__(self, init_pos):
        super(Player, self).__init__()

        # Set the physics of the person
        self.ground = init_pos[1]
        self.init_pos = init_pos
        self.pos = init_pos
        self.y_vel = 0
        self.can_jump = True
        self.jump_vel = 20
        self.gravity = -1

        # Create a Person
        self.size = (PLAYERW,PLAYERH)
        self.person = Rectangle(pos=self.pos, size=self.size)
        self.color = Color(1,0,0)
        self.color_idx = 0
        self.add(self.color)
        self.add(self.person)

    def jump(self):
        if self.can_jump:
            self.y_vel = self.jump_vel
            self.can_jump = False

    def duck(self):
        self.size = (PLAYERW,PLAYERDUCKH)

    def un_duck(self):
        self.size = (PLAYERW,PLAYERH)

    def set_color(self, color_idx):
        self.color_idx = color_idx
        self.color.rgb = COLORS2[color_idx]

    def reset(self):
        self.pos = self.init_pos
        self.y_vel = 0
        self.color.rgb = COLORS2[0]

    def on_update(self, dt):
        # Update position with physics
        self.y_vel += dt*self.gravity
        self.pos = (self.pos[0], max(self.ground,self.pos[1]+dt*self.y_vel))
        if self.pos[1] == self.ground:
            self.can_jump = True
            self.y_vel = 0    
        
        # Update person
        self.person.pos = self.pos
        self.person.size = self.size
