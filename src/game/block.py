class Block(InstructionGroup):
    def __init__(self, init_pos, y, color_idx, translator, width=BLOCK_W, height=BLOCK_H):
        super(Block, self).__init__()

        self.init_pos = init_pos
        self.y = y
        self.width = width
        self.height = height
        self.translator = translator
        self.color = COLORS[color_idx]
        self.color_idx = color_idx
        self.add(self.color)
        self.block = Rectangle(pos=(init_pos, self.y), size=(width, height))
        self.add(self.block)

    def get_current_pos(self):
        return self.init_pos + self.translator.x

    def get_color_idx(self):
        return self.color_idx

    def on_update(self, dt):
        pass