import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *

from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate

class Camera(InstructionGroup):
    def __init__(self, foreground, background):
        super(Camera, self).__init__()

        self.add(background)

        self.translator = Translate(0, 0)
        self.add(self.translator)

        self.add(foreground)

        self.rev_translator = Translate(0, 0)
        self.add(self.rev_translator)

    def move_relative(self, pos):
        x, y = pos
        self.translator.x -= x
        self.translator.y -= y
        self.rev_translator.x += x
        self.rev_translator.y += y

    def move_absolute(self, pos):
        x, y = pos
        self.translator.x = x
        self.translator.y = y
        self.rev_translator.x = -x
        self.rev_translator.y = -y

class Foreground(InstructionGroup):
    def __init__(self, moveable_sprites, terrain):
        super(Foreground, self).__init__()

        self.moveable_sprites = moveable_sprites
        self.terrain = terrain

        self.add(moveable_sprites)
        self.add(terrain)

class Background(InstructionGroup):
    def __init__(self, color):
        super(Background, self).__init__()

        self.add(Color(*color))

        self.rectangle = Rectangle(pos=(0,0), size=Window.size)
        self.add(self.rectangle)

class MovingSprites(InstructionGroup):
    def __init__(self):
        super(MovingSprites, self).__init__()
        self.sprites = []
        self.anim_group = AnimGroup()
        self.add(self.anim_group)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        self.anim_group.add(sprite)

    def on_update(self):
        self.anim_group.on_update()

class Terrain(InstructionGroup):
    def __init__(self):
        super(Terrain, self).__init__()
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)
        self.add(block)

class Sprite(InstructionGroup):
    def __init__(self, source, pos, size):
        super(Sprite, self).__init__()
        self.add(Color(1, 1, 1))
        self.rectangle = Rectangle(source=source, pos=pos,
                              size=size)
        self.add(self.rectangle)