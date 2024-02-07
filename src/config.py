import sys
from pathlib import Path
from typing import NamedTuple


def resource_path(relative_path: Path) -> Path:
    """Function for working paths inside an exe for python."""
    base_path = Path(getattr(sys, "_MEIPASS", ".")).absolute()
    return base_path.joinpath(relative_path)


Size = NamedTuple("Size", (("width", int), ("height", int)))

APP_PATH = resource_path(Path(__file__).parent)

WIDTH, HEIGHT = 520, 725
SIZE = Size(width=WIDTH, height=HEIGHT)
CAPTION = "2048"
FRAMERATE = 120

# game area settings
BLOCKS = 4
SIZE_BLOCK = 112
MARGIN = 9

USERNAME = None
MIN_NAME_LENGTH = 3

images_source_folder_name = "images"

bg_images_name = "BG"
elements = "elements"

icon_name = "icon.png"
icon_folder_name = "icons"

ICON_PATH = resource_path(Path(images_source_folder_name) / Path(icon_folder_name) / Path(icon_name))
BG_PATH = resource_path(Path(images_source_folder_name) / Path(bg_images_name))
ELEMENTS_PATH = resource_path(Path(images_source_folder_name) / Path(elements))

GENERAL_FONT = APP_PATH / "vag-world-bold.ttf"  # The main font of the game

COLORS = {
    0: "#545c8a",
    2: "#e4f2fd",
    4: "#badffa",
    8: "#6cb8f4",
    16: "#319eef",
    32: "#2a79d8",
    64: "#275ce6",
    128: "#7420e8",
    256: "#9025c0",
    512: "#b32885",
    1024: "#990066",
    2048: "#bb165b",
    4096: "#1A0553",
    8192: "#02334D",
    16384: "#004949",
    32768: "#1F142F",
    65536: "#000000",
    131072: "#000000",
    262144: "#000000",
    524288: "#000000",
    "WTF?!": "#ffffff",
    "WHITE": "#ebeeff",
    "GRAY": "#aebad0",
}
