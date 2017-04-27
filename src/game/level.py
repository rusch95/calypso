from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from colors import *
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

        self.direction = 1
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
            start = float(platforms[i][0])*SPACING
            if i < len(platforms)-1:
                end = float(platforms[i+1][0])*SPACING
            else:
                end = start + 1000
            colors = {'r':0,'g':1,'b':2}
            color_idx = colors[platforms[i][1]]
            platform = Platform(start, end, color_idx, self.translator)
            self.platform_list.append(platform)
            self.add(platform)

    def create_jumps(self, jumps):
        for t in jumps:
            pos = float(t)*SPACING
            jump = JumpBlock(pos, 3, self.translator)
            self.jumps.append(jump)
            self.add(jump)

    def create_ducks(self, ducks):
        for t in ducks:
            pos = float(t)*SPACING
            duck = DuckBlock(pos, 3, self.translator)
            self.ducks.append(duck)
            self.add(duck)

    def reverse(self):
        self.direction = -1

    def forward(self):
        self.direction = 1

    def lose(self):
        self.direction = 0
        self.alive = False

    def reset(self):
        self.translator.x = 0
        self.direction = 1
        self.alive = True

    def get_current_platform(self):
        for p in self.platform_list:
            start,end = p.get_current_pos()
            if PLAYERX >= start and PLAYERX < end:
                return p
        return None

    def is_current_duck(self):
        for b in self.ducks:
            pos = b.get_current_pos()
            if pos > PLAYERX-PLAYERW and pos < PLAYERX+DUCKBOXW:
                return True
        return False

    def is_current_jump(self):
        for b in self.jumps:
            pos = b.get_current_pos()
            if pos > PLAYERX-PLAYERW and pos < PLAYERX+JUMPBOXW:
                return True
        return False

    def is_between_platforms(self):
        border = self.get_current_platform().get_current_pos()[1]
        if border < PLAYERX+PLAYERW and border > PLAYERX:
            return True
        else:
            return False

    def on_update(self, dt):
        self.translator.x -= self.direction*SPEED


class Platform(InstructionGroup):
    def __init__(self, init_pos, final_pos, color_idx, translator):
        super(Platform, self).__init__()

        self.init_pos = init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.width = final_pos - init_pos
        self.platform = Rectangle(pos=(init_pos,FLOOR-PLATFORMH), size=(self.width, PLATFORMH))
        self.add(self.platform)

    def get_current_pos(self):
        return (self.init_pos+self.translator.x, self.init_pos+self.width+self.translator.x)

    def on_update(self, dt):
        pass

class JumpBlock(InstructionGroup):
    def __init__(self, init_pos, color_idx, translator):
        super(JumpBlock, self).__init__()

        self.init_pos = init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos,JUMPBOXY), size=(JUMPBOXW, JUMPBOXH))
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
        self.block = Rectangle(pos=(init_pos,DUCKBOXY), size=(DUCKBOXW, DUCKBOXH))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def on_update(self, dt):
        pass

