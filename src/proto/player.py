from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate

class Player(InstructionGroup):
    def __init__(self, init_pos, camera, collision, controller):
        super(Player, self).__init__()

        self.pos = init_pos
        self.y_vel = 0

        self.size = (50, 50)

        self.sprite = Rectangle(pos=init_pos, size=self.size)
        self.add(Color(1, 0, 0))
        self.add(self.sprite)

        self.controller = controller
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
            if key in self.controller.active_keys and self.controller.active_keys[key]:
                delta_x = value
        
        new_pos = x + delta_x, y + delta_y
        down_collision = self.collision.check_down_collision(self.pos, new_pos, self.size)

        if self.collision.check_side_collision(self.pos, new_pos, self.size):
            self.can_jump = True
            self.jump_f *= .95
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
            g = -1300
            self.y_vel = max(self.y_vel + g * dt, terminal_vel)
