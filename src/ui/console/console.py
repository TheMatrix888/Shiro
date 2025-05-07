from .console_object import ConsoleObject
from .window_controller import get_console_window_controller
from .cursor_control import overwrite_line

class Console:
    def __init__(self, console_settings: dict):
        self.buffer_old = None
        self.buffer_new = None
        self._window = get_console_window_controller()
        self.lines = console_settings["lines"]
        self.columns = console_settings["columns"]
        if console_settings["force_window_position"]:
            self.set_position(console_settings["window_x"], console_settings["window_y"])
        self.set_size(self.columns, self.lines)

    def set_position(self, window_x: int, window_y: int):
        self._window.set_position(window_x, window_y)

    def set_size(self, columns: int, lines: int):
        self._window.set_size(columns, lines)
        self.columns = columns
        self.lines = lines
        self.buffer_old = [" " * columns for _ in range(lines)]
        self.buffer_new = [" " * columns for _ in range(lines)]

    def draw(self, x: int, y: int, console_object: ConsoleObject, overlap: bool = False):
        for object_line, in range(0, console_object.height):
            console_line = object_line + y
            if console_line < 0:
                continue
            if console_line >= self.lines:
                break
            line = list(self.buffer_new[console_line])
            for object_column in range(0, console_object.width):
                console_column = object_column + x
                if console_column < 0:
                    continue
                if console_column >= self.columns:
                    break
                if overlap:
                    line[console_column] = console_object.content[object_line][object_column]
                else:
                    if line[console_column] == " ":
                        line[console_column] = console_object.content[object_line][object_column]
            self.buffer_new[console_line] = "".join(line)

    def update(self):
        for line in range(0, self.lines):
            if self.buffer_old[line] != self.buffer_new[line]:
                overwrite_line(line, self.buffer_new[line])
                self.buffer_old[line] = self.buffer_new[line]