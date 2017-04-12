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

        self.background = background
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

        self.background.move_relative(pos)

    def move_absolute(self, pos):
        #TODO Add support for parallax backgroun to handle absolute moves
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

class ParallaxBackground(InstructionGroup):
    def __init__(self):
        super(ParallaxBackground, self).__init__()
        self.layers = []

    def move_relative(self, pos):
        for layer in self.layers:
            layer.move_relative(pos)

    def add_layer(self, layer):
        self.layers.append(layer)
        self.add(layer)

class ParallaxLayer(InstructionGroup):
    def __init__(self, speed):
        super(ParallaxLayer, self).__init__()
        self.speed = speed
        self.translator = Translate(0, 0)
        self.add(self.translator)

        self.objects = InstructionGroup()
        self.add(self.objects)

        self.rev_translator = Translate(0, 0)
        self.add(self.rev_translator)

    def add_object(self, thing):
        self.objects.add(thing)

    def move_relative(self, pos):
        x, y = pos
        self.translator.x -= x * self.speed
        self.translator.y -= y * self.speed
        self.rev_translator.x += x * self.speed
        self.rev_translator.y += y * self.speed

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