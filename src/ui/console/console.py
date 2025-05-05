from .window_controller import get_console_window_controller


class Console:
    def __init__(self, console_settings: dict):
        self.columns = console_settings["columns"]
        self.lines = console_settings["lines"]
        self._window = get_console_window_controller()
        if console_settings["force_window_position"]:
            self.set_position(console_settings["window_x"], console_settings["window_y"])
        self.set_size(self.columns, self.lines)

    def set_position(self, x: int, y: int):
        self._window.set_position(x, y)

    def set_size(self, columns: int, lines: int):
        self._window.set_size(columns, lines)
        self.columns = columns
        self.lines = lines

    def draw(self, object: ):