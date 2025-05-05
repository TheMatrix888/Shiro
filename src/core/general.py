from pathlib import Path
from random import choice, sample
from socket import create_connection
from typing import Any, List


def recursive_directory_walk(directory_path: Path, ends_with: List[str] = None) -> List[Path]:
    if not ends_with:
        return [file for file in directory_path.rglob('*') if file.is_file()]
    else:
        return [file for file in directory_path.rglob('*') if file.is_file() and file.suffix.lower() in ends_with]


def random_element(data: list | dict) -> Any:
    if isinstance(data, list):
        return choice(data)
    elif isinstance(data, dict):
        key = choice(list(data.keys()))
        return key, data[key]


def random_elements(data: list | dict, count: int) -> list:
    if isinstance(data, dict):
        values = list(data.values())
    else:
        values = data
    return sample(values, count)


def is_connected() -> bool:
    try:
        create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False
