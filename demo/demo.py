from time import sleep

from src.ui.console import Console
from src.ui.console.objects import Circle


def pulse(console: Console, max_radius: int):
    def draw_pulse(radius: int):
        circle = Circle(radius=radius, symbol=f"{radius % 10}", console=console)
        x = (console.columns - circle.width) // 2
        y = (console.lines - circle.height) // 2
        circle.draw(x, y)
        console.update()
        sleep(0.1)

    for radius in range(1, max_radius):
        draw_pulse(radius=radius)
    for radius in range(max_radius, 0, -1):
        console.clear()
        draw_pulse(radius=radius)
    console.clear()


settings = {
    "columns": 80,
    "lines": 40,
    "force_window_position": True,
    "window_x": 100,
    "window_y": 100,
}

console = Console(settings)
while input() != "q":
    pulse(console, 20)
