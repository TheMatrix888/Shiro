from abc import abstractmethod
from typing import List

from .console import Console


class ConsoleObject:
    def __init__(self, content: List[str], console: "Console" = None):
        self.content = content
        self.width = max(len(line) for line in content)
        self.height = len(content)
        self.console = console

    def draw(self, x: int, y: int, overlap: bool = False):
        if self.console:
            self.console.draw(x, y, self, overlap)
        else:
            raise ValueError("ConsoleObject must be associated with a Console instance to draw.")

    @abstractmethod
    def generate_content(self) -> List[str]:
        raise NotImplementedError("Subclasses must implement generate_content method.")


class Circle(ConsoleObject):
    def __init__(self, radius: int, symbol: str, console: "Console" = None):
        self.radius = radius
        self.symbol = symbol
        super().__init__(self.generate_content(), console)

    def generate_content(self) -> List[str]:
        circle = []
        for y in range(-self.radius, self.radius + 1):
            line = []
            for x in range(-self.radius, self.radius + 1):
                if x ** 2 + y ** 2 <= self.radius ** 2:
                    line.append(self.symbol)
                else:
                    line.append(" ")
            circle.append("".join(line))
        return circle
