from barline import *
from block import *
from checkpoint import *


def convert_tick_to_x(tick, include_player_x=True):
    return tick * 4 / 15 + PLAYER_X*include_player_x

def convert_x_to_tick(x, include_player_x=False):
    return (x-PLAYER_X*include_player_x) * 15 / 4


class Level(InstructionGroup):
    def __init__(self, platform_messages):
        super(Level, self).__init__()

        self.translator = Translate()

        self.add(self.translator)
        self.checkpoints = []
        self.blocks = []

        self.checkpoints = []
        self.blocks = []

        self.barlines = []

        for i in xrange(0, PLAYER_X + 1, PIXEL):
            start_block = Block(init_pos=i, y=PIXEL, color_idx=RED_IDX, translator=self.translator)
            self.add(start_block)
            self.blocks.append(start_block)

        where_started = {}
        velocities = {}
        for msg in platform_messages:
            if msg.type == 'NoteOnEvent':
                where_started[msg.pitch] = msg.tick
                velocities[msg.pitch] = msg.velocity
            elif msg.type == 'NoteOffEvent':
                begin = convert_tick_to_x(where_started[msg.pitch])
                end = convert_tick_to_x(msg.tick)

                CHECKPOINT_PITCH = 0
                COLORS_MIDI = [WHITE_IDX, RED_IDX, GREEN_IDX, BLUE_IDX, WHITE_IDX, WHITE_IDX]

                if msg.pitch == CHECKPOINT_PITCH:
                    cp = CheckPoint(end, self.translator)
                    self.add(cp)
                    self.checkpoints.add(cp)
                elif msg.pitch >= 12:
                    print msg, begin * 1. / PIXEL, end * 1. / PIXEL
                    block_len = (end - begin) / 64
                    height = msg.pitch / 6 - 1

                    color_idx = msg.pitch % 6
                    color = COLORS_MIDI[color_idx]

                    velocity = velocities[msg.pitch]
                    
                    for i in xrange(block_len):
                        block = Block(init_pos=begin + i * PIXEL, y=height * PIXEL, color_idx=color,
                                      translator=self.translator, velocity=velocity)
                        self.blocks.append(block)
                        self.add(block)

        check_nums = xrange(0,512,32)
        for cn in check_nums:
            checkpoint = CheckPoint(cn*PIXEL + PLAYER_X - 512, self.translator)
            self.add(checkpoint)
            self.checkpoints.append(checkpoint)

        for i in xrange(120):
            xbar = 512 * i + PLAYER_X
            self.bar = Barline(xbar, self.translator)
            self.add(self.bar)
            self.barlines.append(self.bar)

        self.moving_blocks = []
        moving_block = Block(17 * PIXEL, 4 * PIXEL, WHITE_IDX, self.translator, moving=True)
        self.add(moving_block)
        self.blocks.append(moving_block)
        self.moving_blocks.append(moving_block)

        self.direction = 0
        self.alive = True
        self.checkpoint_pos = 0
        self.checkpoint_y = PIXEL * 2
        self.checkpoint_color = RED_IDX
        self.checkpoint_y_vel = 0
        self.checkpoint = self.checkpoints[0]

        # barline that is highlighted for reversal
        self.reverse_line = None

    def get_current_blocks(self):
        current_blocks = []
        for b in self.blocks:
            b_pos = b.get_current_pos()
            if b_pos + b.width >= PLAYER_X and b_pos <= PLAYER_X + PLAYER_W:
                current_blocks.append(b)
        return current_blocks

    def check_checkpoint(self, player_y, color_idx, y_vel):
        for c in self.checkpoints:
            c_pos = c.get_current_pos()
            if c_pos + BAR_W >= PLAYER_X and c_pos <= PLAYER_X + PLAYER_W and c != self.checkpoint:
                print "checkpoint ready"
                self.checkpoint_pos = self.translator.x
                self.checkpoint_y = player_y
                self.checkpoint_color = color_idx
                self.checkpoint_y_vel = y_vel
                self.checkpoint.unset_checkpoint()
                self.checkpoint = c
                self.checkpoint.set_checkpoint()
                self.checkpoint_dir = self.direction

    def reverse(self):
        if self.alive:
            self.direction = -1
            if self.reverse_line:
                self.reverse_line.un_highlight()

    def set_next_barline(self):
        if self.reverse_line:
            self.reverse_line.un_highlight()
        idx = int(-self.translator.x/512)+1
        self.reverse_line = self.barlines[idx]
        self.reverse_line.highlight()

    def forward(self):
        if self.alive:
            self.direction = 1
            if self.reverse_line:
                self.reverse_line.un_highlight()

    def set_previous_barline(self):
        if self.reverse_line:
            self.reverse_line.un_highlight()
        idx = int(-self.translator.x/512)
        self.reverse_line = self.barlines[idx]
        self.reverse_line.highlight()

    def lose(self):
        self.direction = 0
        self.alive = False

    def reset(self):
        self.translator.x = self.checkpoint_pos
        self.direction = 0
        self.alive = True
        if self.reverse_line:
            self.reverse_line.un_highlight()
        return self.checkpoint_y, self.checkpoint_color, self.checkpoint_y_vel, convert_x_to_tick(self.checkpoint_pos)

    def start(self):
        self.direction = 1

    def on_update(self, loc=None):
        if self.alive:
            for block in self.moving_blocks:
                block.on_update()

            if loc is not None:
                self.translator.x = convert_tick_to_x(loc, False)
                # print "on_update", self.translator.x, loc
            else:
                self.translator.x -= self.direction * SPEED

