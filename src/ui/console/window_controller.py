import os
import platform
import ctypes
from ctypes import wintypes

class ConsoleWindowController:
    def set_position(self, x: int, y: int):
        raise NotImplementedError

    def set_size(self, columns: int, lines: int):
        raise NotImplementedError


class WindowsConsoleWindowController(ConsoleWindowController):
    def set_position(self, x: int, y: int):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        ctypes.windll.user32.MoveWindow(hwnd, x, y, width, height, True)

    def set_size(self, columns: int, lines: int):
        os.system(f"mode con: cols={columns} lines={lines}")


class LinuxConsoleWindowController(ConsoleWindowController):
    def __init__(self):
        if os.system("which xdotool > /dev/null 2>&1") != 0:
            raise RuntimeError("xdotool not found. Please install it to use window positioning on Linux.")

    def set_position(self, x: int, y: int):
        os.system(f"xdotool getactivewindow windowmove {x} {y}")

    def set_size(self, columns: int, lines: int):
        # Expands buffer and window, doesn't work for all terminals
        print(f"\033[8;{lines};{columns}t")


class DummyConsoleWindowController(ConsoleWindowController):
    def set_position(self, x: int, y: int):
        print(f"[INFO] set_position({x}, {y}) not supported on this OS.")

    def set_size(self, columns: int, lines: int):
        print(f"[INFO] set_size({columns}, {lines}) not supported on this OS.")


def get_console_window_controller() -> ConsoleWindowController:
    system = platform.system()
    if system == "Windows":
        return WindowsConsoleWindowController()
    elif system == "Linux":
        try:
            return LinuxConsoleWindowController()
        except RuntimeError as exception:
            print(f"[WARN] {exception}")
    return DummyConsoleWindowController()
