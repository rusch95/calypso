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
from player import *
from graphics import *

import pdb

Window.size = (1024, 768)

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.controller = Controller()
        self.collision = CollisionMesh()

        self.background = Background((0, 0.3, 0.6))

        self.movable_sprites = MovingSprites()
        self.terrain = self.setup_level()
        self.foreground = Foreground(self.movable_sprites, self.terrain)

        self.camera = Camera(self.foreground, self.background)
        self.canvas.add(self.camera)

        self.player = Player((300, 200), self.camera, self.collision, self.controller)
        self.movable_sprites.add_sprite(self.player)

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
        self.info.text = '\nfps:%d' % kivyClock.get_fps()

run(MainWidget)

