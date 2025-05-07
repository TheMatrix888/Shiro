def move_cursor_to(line: int, column: int):
    print(f"\033[{line};{column}H", end="")

def clear_line():
    print("\033[K", end="")

def overwrite_text(line: int, column: int, text: str):
    move_cursor_to(line, column)
    clear_line()
    print(text, end="")

def overwrite_line(line: int, text: str):
    overwrite_text(line, 1, text)
