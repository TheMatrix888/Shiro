import pytest
from src.ui.console import Console

def test_console_creation():
    console = Console()
    assert console is not None