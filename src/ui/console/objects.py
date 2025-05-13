from typing import List

from .console import Console
from .console_object import ConsoleObject

ASPECT_RATIO = 2  # Adjust this ratio to fit your console's character aspect ratio


class Circle(ConsoleObject):
    def __init__(self, radius: int, symbol: str, console: Console = None):
        self.radius = radius
        self.symbol = symbol
        super().__init__(self.generate_content(), console)

    def generate_content(self) -> List[str]:
        circle = []
        for y in range(-self.radius, self.radius + 1):
            line = []
            for x in range(-self.radius, self.radius + 1):
                if x ** 2 + (y ** 2) * ASPECT_RATIO <= self.radius ** 2:
                    line.append(self.symbol)
                else:
                    line.append(" ")
            circle.append("".join(line))
        return circle