from kivy.graphics import Color, Ellipse, Rectangle, Line
from graphics import *
from collision import *

import math

def setup_level(collision):
    terrain = Terrain()

    rectangles = [((10, 50), (600, 30)),
                    ((600, 120), (800, 30)),
                    ((1400, 85), (600, 30)),
                    ((2200, 150), (200, 30)),
                    ((2500, 200), (200, 30)),
                    ((2800, 250), (200, 30))]

    #landscape = [50, 100, 90, 80, 69, 75, 90, 110, 135, 150, 170, 188, 150, 100 , 53, 500]
    #for i, y in enumerate(landscape):
    #    left_x = 500 + i * 100
    #    size_x = 100
    #    rect = ((left_x, 0), (size_x, y+200))
    #    rectangles.append(rect)

    terrain.add_block(Color(0, .2, 0))
    for pos, size in rectangles:
        rect = Rectangle(pos=pos, size=size)
        terrain.add_block(rect)
        collision.add_rectangle(pos, size)

    return terrain

class Collectables(InstructionGroup):
    def __init__(self, player):
        super(Collectables, self).__init__()

        self.collectable_collision = NewCollisionMesh()
        self.player = player

        for x in [i * 100 for i in xrange(20)]:
            pos = (x, 400)
            size = (30, 30)
            collectable = CollisionSprite(pos=pos, size=size)
            self.add(Color(1, 1, 0))
            self.add(collectable)
            self.collectable_collision.add(collectable)

    def on_update(self, dt):
        collisions = self.collectable_collision.check_collision(self.player.pos, self.player.pos, self.player.size)
        for collision in collisions:
            self.remove(collision)
            self.collectable_collision.remove(collision)

class BulletStorm(InstructionGroup):
    def __init__(self, player):
        super(BulletStorm, self).__init__()

        self.frame = 0

        self.bullet_collision = NewCollisionMesh()
        self.player = player
        for pos in [(1000, 300), (1200, 300), (800, 400), (500, 500)]:
            size = (30, 30)
            bullet = Bullet(pos=pos, size=size)
            self.add(Color(1, 1, 0))
            self.add(bullet)
            self.bullet_collision.add(bullet)

    def on_update(self, dt):
        collisions = self.bullet_collision.check_collision(self.player.pos, self.player.pos, self.player.size)
        for collision in collisions:
            self.bullet_collision.remove(collision)
            self.remove(collision)

        for bullet in self.children:
            if isinstance(bullet, Bullet):
                bullet.on_update(dt)

        self.frame += 1
        if self.frame % 1 == 0:
            y = (math.sin(self.frame / 30.) + 1) * 200 + 150
            bullet = Bullet(pos=(1500, y), size=(20, 20))
            hue = (self.frame / 100.) % 1
            self.add(Color(hue, 1, 1, mode='hsv'))
            self.add(bullet)
            self.bullet_collision.add(bullet)
        
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