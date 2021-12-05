import config
from game import Game


class Interface(Game):
    def __init__(self):
        super().__init__(config.CAPTION, config.WIDTH, config.HEIGHT, config.ICON, config.FRAMERATE)
        self.blocks = config.BLOCKS
        self.size_block = config.SIZE_BLOCK
        self.margin = config.MARGIN
        self.generalFont = config.GENERAL_FONT
