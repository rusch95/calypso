from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from colors import *

SPEED = 5
SPACING = SPEED*60

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
            self.add(platform)

    def create_jumps(self, jumps):
        for t in jumps:
            pos = float(t)*SPACING
            jump = JumpBlock(pos, 3, self.translator)
            self.add(jump)

    def create_ducks(self, ducks):
        for t in ducks:
            pos = float(t)*SPACING
            duck = DuckBlock(pos, 3, self.translator)
            self.add(duck)

    def on_update(self, dt):
        self.translator.x -= SPEED


class Platform(InstructionGroup):
    def __init__(self, init_pos, final_pos, color_idx, translator):
        super(Platform, self).__init__()

        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.width = final_pos - init_pos
        self.platform = Rectangle(pos=(init_pos,50), size=(self.width, 50))
        self.add(self.platform)

    def on_update(self, dt):
        pass

class JumpBlock(InstructionGroup):
    def __init__(self, init_pos, color_idx, translator):
        super(JumpBlock, self).__init__()

        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos,100), size=(50, 50))
        self.add(self.block)

    def on_update(self, dt):
        pass

class DuckBlock(InstructionGroup):
    def __init__(self, init_pos, color_idx, translator):
        super(DuckBlock, self).__init__()
        print init_pos
        self.translator = translator
        self.color = COLORS[color_idx]
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos,200), size=(50, 50))
        self.add(self.block)

    def on_update(self, dt):
        pass

