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
        self.collision = CollisionMesh()

        self.background = parallax()

        self.movable_sprites = MovingSprites()
        self.terrain = setup_level(self.collision)
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

def parallax():
    parallax_background = ParallaxBackground()

    layer1 = ParallaxLayer(0)
    base = InstructionGroup()
    base.add(Color(1,1,1))
    base.add(Sprite(source='../../data/background.png', pos=(0,0), size=Window.size))
    layer1.add_object(base)
    
    trees = InstructionGroup()
    tree_paths = ['../../data/tree{}.png'.format(i) for i in xrange(1,4)] 
    for i, path in enumerate(tree_paths):
        trees.add(Sprite(source=path, pos=(i * 500, -100), size=(500, 500)))
    layer2 = ParallaxLayer(.2)
    layer2.add_object(trees)

    parallax_background.add_layer(layer1)
    parallax_background.add_layer(layer2)

    return parallax_background

run(MainWidget)

