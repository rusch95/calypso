import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *

from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate

from controller import *
from collision import *
from graphics import *
from level import *
from player import *

import pdb

Window.size = (1024, 768)

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.controller = Controller()
        self.terrain_collision = CollisionMesh()

        self.background = parallax()

        self.movable_sprites = MovingSprites()
        self.terrain = setup_level(self.terrain_collision)
        self.foreground = Foreground(self.movable_sprites, self.terrain)

        self.camera = Camera(self.foreground, self.background)
        self.canvas.add(self.camera)

        self.player = Player((300, 200), self.camera, self.terrain_collision, self.controller)
        self.movable_sprites.add_sprite(self.player)

        self.movable_sprites.add_sprite(Collectables(self.player))
        self.movable_sprites.add_sprite(BulletStorm(self.player))

        self.info = topleft_label()
        self.add_widget(self.info)

        
    def on_key_down(self, keycode, modifiers):
        self.controller.active_keys[keycode[1]] = True

        if keycode[1] == 'z':
            self.player.jump()

    def on_key_up(self, keycode):
        self.controller.active_keys[keycode[1]] = False

    def on_update(self):
        self.movable_sprites.on_update()
        self.info.text = 'fps:%d' % kivyClock.get_fps()

run(MainWidget)

