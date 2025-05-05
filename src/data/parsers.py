from datetime import datetime

from src.shiro.config import ASCII_IMAGES_FILES, KAOMOJIS_FILE, LAST_ACTIONS_FILE, SETTINGS_FILE
from src.json_utils import read_json


def parse_settings():
    settings_data = read_json(SETTINGS_FILE)
    services = settings_data["services"]
    return (
        settings_data["user"],
        settings_data["console"],
        settings_data["ascii_art"],
        services["genius_bot"],
        services["check_in"]
    ) if settings_data else None


def parse_ascii_images():
    return {
        ascii_image_file.stem: {
            "ascii_str": data["ascii_str"],
            "colors": data["colors"]
        }
        for ascii_image_file in ASCII_IMAGES_FILES
        for data in [read_json(ascii_image_file)]
    }


def parse_last_actions():
    data = read_json(LAST_ACTIONS_FILE)
    last_post = datetime.fromisoformat(data["last_post"])
    last_check_in = datetime.fromisoformat(data["last_check_in"])
    return last_post, last_check_in


def parse_kaomojis():
    return read_json(KAOMOJIS_FILE)
