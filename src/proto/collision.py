from kivy.core.window import Window

class CollisionRect(object):
    def __init__(self, left_x, bottom_y, right_x, top_y):
        self.left_x = left_x
        self.bottom_y = bottom_y
        self.right_x = right_x
        self.top_y = top_y

    def check_down_collision(self, old_pos, new_pos, size):
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