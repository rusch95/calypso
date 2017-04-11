

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
        self.camera = Camera()

        self.canvas.add(self.camera)

        self.anim_group = AnimGroup()
        self.canvas.add(self.anim_group)

        self.collision = CollisionMesh()
        self.player = Player((50, 200), self.camera, self.collision)
        self.anim_group.add(self.player)

        self.setup_level()


    def setup_level(self):
        rectangles = [((10, 50), (600, 30)),
                      ((600, 120), (800, 30)),
                      ((1400, 85), (600, 30)),
                      ((2200, 150), (200, 30)),
                      ((2500, 200), (200, 30)),
                      ((2800, 250), (200, 30))]

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

    def check_collision(self, old_pos, new_pos):
        #TODO Support collisions besides top down
        ox, oy = old_pos
        nx, ny = new_pos

        if self.left_x <= nx <= self.right_x and ny <= self.top_y and oy >= self.top_y:
            return self.top_y 

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

    def check_collision(self, old_pos, new_pos):
        for rect in self.collision_rects:
            collision = rect.check_collision(old_pos, new_pos) 
            if collision:
                return collision

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

        self.sprite = Rectangle(pos=init_pos, size=(10, 30))
        self.add(Color(1, 0, 0))
        self.add(self.sprite)

        self.collision = collision
        self.camera = camera

        self.can_jump = True

    def move_absolute(self, pos):
        self.pos = pos

    def move_relative(self, pos):
        x, y = pos
        old_x, old_y = self.pos
        self.pos = (x + old_x, y + old_y)

        self.sprite.pos = self.pos

    def jump(self):
        if self.can_jump > 0:
            self.y_vel = 800
            self.can_jump -= 1

    def on_update(self, dt):
        alpha = 200
        delta = dt * alpha
        key_mappings = {'left':   (-delta, 0),
                        'right':  (delta, 0)}

        for key, value in key_mappings.items():
            if key in active_keys and active_keys[key]:
                x, y = value
                self.camera.move_relative(value)
                self.move_relative(value)
        
        y_offset = self.y_vel * dt
        x, y = self.pos
        new_pos = x, y + y_offset
        collision = self.collision.check_collision((x,y), new_pos)
        if collision:
            self.can_jump = 2
            self.y_vel = 0
            self.move_absolute((x, collision))
        else:
            self.move_relative((0, y_offset))

            g = -1000
            self.y_vel = max(self.y_vel + g * dt, -1000)


run(MainWidget)

