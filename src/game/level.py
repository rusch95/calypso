from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *


class Level(InstructionGroup):
    def __init__(self, text_file):
        super(Level, self).__init__()

        self.translator = Translate()
        self.add(self.translator)

        self.jump_times = None
        self.duck_times = None
        self.platforms = None

        self.read_level_data(text_file)
        self.create_ducks(self.duck_times)
        self.create_jumps(self.jump_times)
        self.create_platforms(self.platforms)

        # self.bar = Barline(500, self.translator)
        # self.add(self.bar)

        #self.move = VMovingBlock(500, self.translator)
        #self.add(self.move)

        self.direction = 0
        self.alive = True

    def read_level_data(self, filepath):
        # read text file
        file = open(filepath)
        lines = file.readlines()
        jumps = []
        ducks = []
        platforms = []
        # Sort text file
        for line in lines:
            time,obj = line.split()
            if obj == 'u':
                jumps.append(time)
            elif obj == 'd':
                ducks.append(time)
            else:
                platforms.append([time,obj])

        # Store Values
        self.jump_times = jumps
        self.duck_times = ducks
        self.platforms = platforms

        # Store Objects
        self.platform_list = []
        self.jumps = []
        self.ducks = []

    def create_platforms(self, platforms):
        for i in xrange(len(platforms)):
            start = float(platforms[i][0]) * SPACING
            if i < len(platforms)-1:
                end = float(platforms[i+1][0]) * SPACING
            else:
                end = start + 1000
            colors = {'r':0,'g':1,'b':2}
            color_idx = colors[platforms[i][1]]
            platform = Platform(start, end, color_idx, self.translator)
            self.platform_list.append(platform)
            self.add(platform)

    def create_jumps(self, jumps):
        for t in jumps:
            pos = float(t) * SPACING
            jump = JumpBlock(pos, 3, self.translator)
            self.jumps.append(jump)
            self.add(jump)

    def create_ducks(self, ducks):
        for t in ducks:
            pos = float(t) * SPACING
            duck = DuckBlock(pos, 3, self.translator)
            self.ducks.append(duck)
            self.add(duck)

    def reverse(self):
        if self.alive:
            self.direction = -1

    def forward(self):
        if self.alive:
            self.direction = 1

    def lose(self):
        self.direction = 0
        self.alive = False

    def reset(self):
        self.translator.x = 0
        self.direction = 0
        self.alive = True

    def start(self):
        self.direction = 1

    def get_current_platform(self):
        for p in self.platform_list:
            start,end = p.get_current_pos()
            if PLAYER_X >= start and PLAYER_X < end:
                return p
        return None

    def is_current_duck(self):
        for b in self.ducks:
            pos = b.get_current_pos()
            if pos > PLAYER_X - PLAYER_W and pos < PLAYER_X + DUCK_BOX_W:
                return True
        return False

    def is_current_jump(self):
        for b in self.jumps:
            pos = b.get_current_pos()
            if pos > PLAYER_X - PLAYER_W and pos < PLAYER_X + JUMP_BOX_W:
                return True
        return False

    def is_between_platforms(self):
        border = self.get_current_platform().get_current_pos()[1]
        if border < PLAYER_X + PLAYER_W and border > PLAYER_X:
            return True
        else:
            return False

    def on_update(self, dt):
        self.translator.x -= self.direction * SPEED


class Platform(InstructionGroup):
    def __init__(self, init_pos, final_pos, color_idx, translator):
        super(Platform, self).__init__()

        self.init_pos = init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.width = final_pos - init_pos
        self.platform = Rectangle(pos=(init_pos, FLOOR - PLATFORM_H), size=(self.width, PLATFORM_H))
        self.add(self.platform)

    def get_current_pos(self):
        return (self.init_pos + self.translator.x, self.init_pos + self.width + self.translator.x)

    def on_update(self, dt):
        pass


class JumpBlock(InstructionGroup):
    def __init__(self, init_pos, color_idx, translator):
        super(JumpBlock, self).__init__()

        self.init_pos = init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos, JUMP_BOX_Y), size=(JUMP_BOX_W, JUMP_BOX_H))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self, dt):
        pass


class DuckBlock(InstructionGroup):
    def __init__(self, init_pos, color_idx, translator):
        super(DuckBlock, self).__init__()
        
        self.init_pos = init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos, DUCK_BOX_Y), size=(DUCK_BOX_W, DUCK_BOX_H))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self, dt):
        pass

class Barline(InstructionGroup):
    def __init__(self, init_pos, translator):
        self.init_pos = init_pos
        self.translator = translator
        self.color = GREY
        self.add(self.color)
        self.bar = Rectangle(pos=(init_pos,BAR_Y), size=(BAR_W, BAR_H))
        self.add(self.bar)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self, dt):
        pass

class VMovingBlock(InstructionGroup):
    def __init__(self, init_pos, translator, init_y=FLOOR, speed=V_M_BOX_SPEED):
        self.init_pos = init_pos
        self.y = init_y
        self.translator = translator
        self.color = WHITE
        self.add(self.color)
        self.box = Rectangle(pos=(init_pos,self.y), size=(V_M_BOX_W, V_M_BOX_H))
        self.add(self.box)

        self.up = True
        self.speed = speed

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self, dt):
        # update direction
        if self.y > V_M_BOX_Y_MAX:
            self.up = False
        if self.y < V_M_BOX_Y_MIN:
            self.up = True
        # update y
        if self.up:
            self.y += self.speed
        else:
            self.y -= self.speed