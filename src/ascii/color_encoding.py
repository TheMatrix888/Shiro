from base64 import b64decode, b64encode
from typing import List


def encode_color(r: int, g: int, b: int) -> str:
    return b64encode(bytearray([r, g, b])).decode()


def decode_color(encoded_color: str) -> List[int]:
    color = b64decode(encoded_color)
    return [color[0], color[1], color[2]]


def decode_colors(encoded_colors: str) -> List[List[int]]:
    colors = [encoded_colors[i:i + 4] for i in range(0, len(encoded_colors), 4)]
    return [decode_color(color) for color in colors]
