

import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *

from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate

Window.size = (1024, 768)
active_keys = {}

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.background = Rectangle(pos=(0,0), size=Window.size)
        self.canvas.add(Color(0, 0.3, 0.6))
        self.canvas.add(self.background)

        self.canvas.add(Color(1, 1, 1))
        angry_sun = Rectangle(source='../../data/angry_sun.png', pos=(150, 600),
                              size=(100, 100))
        self.canvas.add(angry_sun)

        cloud_pos = [(200, 500), (400, 567), (900, 413)]
        for pos in cloud_pos:
            cloud = Rectangle(source='../../data/cloud.png', pos=pos,
                               size=(200, 100))
            self.canvas.add(cloud)

        self.camera = Camera()
        self.canvas.add(self.camera)

        self.anim_group = AnimGroup()
        self.canvas.add(self.anim_group)

        self.collision = CollisionMesh()
        self.player = Player((300, 200), self.camera, self.collision)
        self.anim_group.add(self.player)

        self.setup_level()


    def setup_level(self):
        rectangles = [((10, 50), (600, 30)),
                      ((600, 120), (800, 30)),
                      ((1400, 85), (600, 30)),
                      ((2200, 150), (200, 30)),
                      ((2500, 200), (200, 30)),
                      ((2800, 250), (200, 30))]

        landscape = [50, 100, 90, 80, 69, 75, 90, 110, 135, 150, 170, 188, 150, 100 , 53, 500]
        for i, y in enumerate(landscape):
            left_x = 500 + i * 100
            size_x = 100
            rect = ((left_x, 0), (size_x, y+200))
            rectangles.append(rect)

        self.canvas.add(Color(0, 1, 0))
        for pos, size in rectangles:
            rect = Rectangle(pos=pos, size=size)
            self.canvas.add(rect)
            self.collision.add_rectangle(pos, size)
        
    def on_key_down(self, keycode, modifiers):
        global active_keys
        active_keys[keycode[1]] = True

        if keycode[1] == 'z':
            self.player.jump()

    def on_key_up(self, keycode):
        global active_keys
        active_keys[keycode[1]] = False

    def update_camera(self):
        delta = 5
        key_mappings = {'up':    (0, -delta),
                        'down':  (0, delta),
                        'left':  (delta, 0),
                       'right': (-delta, 0)}

        for key, value in key_mappings.items():
            if key in active_keys and active_keys[key]:
                self.camera.move_relative(*value)

    def on_update(self):
        #self.update_camera()

        self.anim_group.on_update()

class CollisionRect(object):
    def __init__(self, left_x, bottom_y, right_x, top_y):
        self.left_x = left_x
        self.bottom_y = bottom_y
        self.right_x = right_x
        self.top_y = top_y

    def check_down_collision(self, old_pos, new_pos, size):
        #TODO Support collisions besides top down
        ox, oy = old_pos
        nx, ny = new_pos
        dx, dy = size

        #Rectanglular collision checking
        if self.left_x - dx <= nx <= self.right_x:
            #Simple top collision
            if  oy >= self.top_y and ny <= self.top_y:
                return self.top_y 

        return False

    def check_side_collision(self, old_pos, new_pos, size):
        left_x, bot_y = new_pos
        dx, dy = size
        right_x, top_y = left_x + dx, bot_y + dy

        if self.left_x - dx < left_x < self.right_x:
            if self.bottom_y - dy < bot_y < self.top_y:
                return True
        return False 


class CollisionMesh(object):
    def __init__(self):
        self.collision_rects = []

    def add_rectangle(self, bottom_left_pos, size):
        left_x, bottom_y = bottom_left_pos
        dx, dy = size
        right_x, top_y = left_x + dx, bottom_y + dy

        rect = CollisionRect(left_x, bottom_y, right_x, top_y)

        self.collision_rects.append(rect)

    def check_down_collision(self, old_pos, new_pos, size):
        for rect in self.collision_rects:
            collision = rect.check_down_collision(old_pos, new_pos, size) 
            if collision:
                return collision
        return False

    def check_side_collision(self, old_pos, new_pos, size):
        for rect in self.collision_rects:
            if rect.check_side_collision(old_pos, new_pos, size):
                return True
        return False

class Camera(InstructionGroup):
    def __init__(self):
        super(Camera, self).__init__()

        self.translator = Translate(0, 0)
        self.add(self.translator)

    def move_relative(self, pos):
        x, y = pos
        self.translator.x -= x
        self.translator.y -= y

    def move_absolute(self, pos):
        x, y = pos
        self.translator.x = x
        self.translator.y = y

class Player(InstructionGroup):
    def __init__(self, init_pos, camera, collision):
        super(Player, self).__init__()

        self.pos = init_pos
        self.y_vel = 0

        self.size = (50, 50)

        self.sprite = Rectangle(pos=init_pos, size=self.size)
        self.add(Color(1, 0, 0))
        self.add(self.sprite)

        self.collision = collision
        self.camera = camera

        self.can_jump = True
        self.og_jump_f = 800
        self.jump_f = self.og_jump_f

    def move_absolute(self, pos):
        self.pos = pos

    def move_relative(self, pos):
        x, y = pos
        old_x, old_y = self.pos
        self.pos = (x + old_x, y + old_y)
        self.sprite.pos = self.pos

    def jump(self):
        if self.can_jump > 0:
            self.y_vel = self.jump_f
            self.can_jump -= 1

    def on_update(self, dt):
        terminal_vel = -1000

        x, y = self.pos
        delta_x = 0
        delta_y = self.y_vel * dt

        alpha = 200
        delta = dt * alpha
        key_mappings = {'left':  -delta,
                        'right':  delta}

        for key, value in key_mappings.items():
            if key in active_keys and active_keys[key]:
                delta_x = value
        
        new_pos = x + delta_x, y + delta_y
        down_collision = self.collision.check_down_collision(self.pos, new_pos, self.size)

        if self.collision.check_side_collision(self.pos, new_pos, self.size):
            self.can_jump = True
            self.jump_f *= .9
            terminal_vel = -200
        else:
            self.can_jump = False
            self.camera.move_relative((delta_x, 0))
            self.move_relative((delta_x, 0))
        
        if down_collision:
            self.can_jump = True
            self.y_vel = 0
            self.jump_f = self.og_jump_f
            self.move_relative((0, down_collision - y))
        else:
            self.move_relative((0, delta_y))
            g = -1000
            self.y_vel = max(self.y_vel + g * dt, terminal_vel)


run(MainWidget)

