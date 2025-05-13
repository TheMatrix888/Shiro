from abc import abstractmethod
from typing import List


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
