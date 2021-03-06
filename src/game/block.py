from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics import Translate
from kivy.uix.image import Image

from const import *

texture_paths = ['grayscale_girder.png', 
                 'brick_desat.png',
                 'brick_left_edge_normal_desat.png',
                 'brick_left_edge_top_desat.png',
                 'brick_top_desat.png',
                 'brick_right_edge_top_desat.png',
                 'brick_right_edge_normal_desat.png']

#80 onwards
textures = {i + 80: Image(source='../../data/tiles/{}'.format(texture_paths[i])) 
            for i in xrange(len(texture_paths))}

class Block(InstructionGroup):
    def __init__(self, init_pos, y, color_idx,
                 translator, width=BLOCK_W, height=BLOCK_H,
                 moving=False, miny=BLOCK_MIN, maxy=BLOCK_MAX,
                 speed=BLOCK_SPEED, texture=None, velocity=80):
        super(Block, self).__init__()

        # Store parameters
        self.init_pos = init_pos
        self.init_y = y
        self.y = y
        self.width = width
        self.height = height
        self.translator = translator
        self.color = COLORS[color_idx]
        self.color_idx = color_idx
        self.moving = moving

        if self.moving:
            self.miny = miny
            self.maxy = maxy
            self.speed = speed
            self.up = True

        texture = textures[velocity].texture

        # Create block
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos, self.y), size=(width, height), texture=texture)
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def get_color_idx(self):
        return self.color_idx

    def check_game_loss(self, player):
        if self.color_idx == WHITE_IDX or player.color_idx == self.color_idx:
            player_bottom = player.pos[1]
            player_top = player.pos[1] + player.size[1]
            block_bottom = self.y
            block_top = self.y + self.height
            if player_bottom >= block_top or player_top <= block_bottom:
                return False
            return True
        return False

    def on_ground(self, player):
        ground = self.y + self.height
        if abs(player.pos[1] - ground+18) < 27 and (player.color_idx == self.color_idx or self.color_idx == WHITE_IDX):
            return ground
        return 0

    def reset(self):
        if self.moving:
            self.remove(self.block)
            self.block = Rectangle(pos=(self.init_pos, self.init_y), size=(self.width, self.height))
            self.add(self.block)

    def on_update(self):
        if self.moving:
            # update direction
            if self.y > self.maxy:
                self.up = False
            if self.y < self.miny:
                self.up = True
            # update y
            if self.up:
                self.y += self.speed
            else:
                self.y -= self.speed
            # redraw block
            self.remove(self.block)
            self.block = Rectangle(pos=(self.init_pos, self.y), size=(self.width, self.height))
            self.add(self.block)
