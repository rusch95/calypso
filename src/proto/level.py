from kivy.graphics import Color, Ellipse, Rectangle, Line
from graphics import *

def setup_level(self):
    terrain = Terrain()

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

    terrain.add_block(Color(0, 1, 0))
    for pos, size in rectangles:
        rect = Rectangle(pos=pos, size=size)
        terrain.add_block(rect)
        self.collision.add_rectangle(pos, size)

    return terrain