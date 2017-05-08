from barline import *
from block import *
from checkpoint import *


def convert_tick_to_x(tick):
    return tick * 4 / 15 + PLAYER_X


class Level(InstructionGroup):
    def __init__(self, platform_messages):
        super(Level, self).__init__()

        self.translator = Translate()
        self.add(self.translator)

        self.checkpoints = []
        self.blocks = []

        for i in xrange(0, PLAYER_X + 1, PIXEL):
            start_block = Block(init_pos=i, y=PIXEL, color_idx=RED_IDX, translator=self.translator)
            self.add(start_block)
            self.blocks.append(start_block)

        where_started = {}
        for msg in platform_messages:
            if msg.type == 'NoteOnEvent':
                where_started[msg.pitch] = msg.tick
            elif msg.type == 'NoteOffEvent':
                begin = convert_tick_to_x(where_started[msg.pitch])
                end = convert_tick_to_x(msg.tick)

                CHECKPOINT_PITCH = 0
                COLORS_MIDI = [None, RED_IDX, GREEN_IDX, BLUE_IDX, WHITE_IDX, None]

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

                    for i in xrange(block_len):
                        block = Block(init_pos=begin + i * PIXEL, y=height * PIXEL, color_idx=color,
                                      translator=self.translator)
                        self.blocks.append(block)
                        self.add(block)

        self.checkpoint = CheckPoint(0, self.translator)
        self.add(self.checkpoint)
        self.checkpoints.append(self.checkpoint)

        # self.jump_times = No
        for i in xrange(50):
            xbar = 384 * i
            xcheck = PIXEL * i * 25 + PIXEL * 3
            xr = PIXEL * i
            xg = PIXEL * i + PIXEL * 50
            xb = PIXEL * i + PIXEL * 16
            xl = PIXEL * 16 * i + PIXEL * 16
            xh = PIXEL * 16 * i + PIXEL * 24
            # barlines
            self.bar = Barline(xbar, self.translator)
            self.add(self.bar)

            # self.checkpoint = CheckPoint(xcheck, self.translator)
            # self.add(self.checkpoint)
            # self.checkpoints.append(self.checkpoint)

            ### platforms
            # self.block = Block(xr, PIXEL, RED_IDX, self.translator)
            # self.add(self.block)
            # self.blocks.append(self.block)
            # self.block = Block(xg, PIXEL, GREEN_IDX, self.translator)
            # self.add(self.block)
            # self.blocks.append(self.block)
            # self.block = Block(xb, 3*PIXEL, BLUE_IDX, self.translator)
            # self.add(self.block)
            # self.blocks.append(self.block)

            ### dodge blocks
            # self.block = Block(xl, 2*PIXEL, WHITE_IDX, self.translator)
            # self.add(self.block)
            # self.blocks.append(self.block)
            # self.block = Block(xh, 4*PIXEL, WHITE_IDX, self.translator)
            # self.add(self.block)
            # self.blocks.append(self.block)

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

    def forward(self):
        if self.alive:
            self.direction = 1

    def lose(self):
        self.direction = 0
        self.alive = False

    def reset(self):
        self.translator.x = self.checkpoint_pos
        self.direction = 0
        self.alive = True
        return self.checkpoint_y, self.checkpoint_color, self.checkpoint_y_vel

    def start(self):
        self.direction = 1

    def on_update(self, dt):
        self.translator.x -= self.direction * SPEED
        if self.alive:
            for block in self.moving_blocks:
                block.on_update()
