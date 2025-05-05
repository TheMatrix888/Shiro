from pathlib import Path
from typing import Dict

from PIL import Image

from src.ascii.color_encoding import encode_color


def convert_image_to_ascii(image_path: Path, width: int, height: int, ascii_density: str) -> Dict[str, str]:
    image = Image.open(image_path)
    image = image.resize((width, height))
    gray_image = image.convert("L")
    rgb_image = image.convert("RGB")

    ascii_str = ""
    colors = ""
    for y in range(gray_image.height):
        for x in range(gray_image.width):
            pixel_value = gray_image.getpixel((x, y))
            density_index = int(pixel_value / (255 / len(ascii_density))) - 1
            ascii_char = ascii_density[density_index]
            ascii_str += ascii_char
            r, g, b = rgb_image.getpixel((x, y))
            colors += encode_color(r, g, b)
        ascii_str += "\n"

    return {
        "ascii_str": ascii_str,
        "colors": colors
    }
