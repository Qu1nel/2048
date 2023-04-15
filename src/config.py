import os

APP_PATH = os.path.dirname(os.path.realpath(__file__))
print(APP_PATH)

WIDTH, HEIGHT = 520, 725
CAPTION = '2048'
FRAMERATE = 120

# game area settings
BLOCKS = 4
SIZE_BLOCK = 112
MARGIN = 9

USERNAME = None
GENERAL_FONT = os.path.join(APP_PATH, 'vag-world-bold.ttf')  # The main font of the game
ICON = os.path.join(APP_PATH, '2048_icon.png')

COLORS = {
    0: "#545c8a", 2: '#e4f2fd', 4: '#badffa',
    8: '#6cb8f4', 16: '#319eef', 32: '#2a79d8',
    64: '#275ce6', 128: '#7420e8', 256: '#9025c0',
    512: '#b32885', 1024: '#990066', 2048: '#bb165b',
    4096: '#1A0553', 8192: '#02334D', 16384: '#004949',
    32768: '#1F142F', 65536: '#000000', 131072: '#000000',
    262144: '#000000', 524288: '#000000',
    'WTF?!': '#ffffff', 'WHITE': '#ebeeff', 'GRAY': '#aebad0'
}
