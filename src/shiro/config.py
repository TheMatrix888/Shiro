import sys
from pathlib import Path

from colorama import Back, Fore

from src.core.general import recursive_directory_walk

BASE_DIR = Path(sys.argv[0]).parent.resolve()

RESOURCES_DIR = BASE_DIR / "resources"
ORIGINAL_IMAGES_DIR = RESOURCES_DIR / "original_images"
ASCII_IMAGES_DIR = RESOURCES_DIR / "ascii_arts"

SETTINGS_FILE = RESOURCES_DIR / "settings.json"
KAOMOJIS_FILE = RESOURCES_DIR / "kaomojis.json"
SHIRO_QUOTES_FILE = RESOURCES_DIR / "shiro_quotes.json"
ORIGINAL_IMAGES_FILES = recursive_directory_walk(ORIGINAL_IMAGES_DIR, [".png", ".jpg", ".jpeg"])
ASCII_IMAGES_FILES = recursive_directory_walk(ASCII_IMAGES_DIR, [".json"])
LAST_ACTIONS_FILE = RESOURCES_DIR / "last_actions.json"
GENIUS_MOMENT_FILE = RESOURCES_DIR / "genius_moment.txt"
USED_PHRASES_FILE = RESOURCES_DIR / "used_phrases.txt"
CHROMEDRIVER_FILE = RESOURCES_DIR / "chromedriver.exe"
SILENT_DRIVER = True

SERVICE_NAME = "Shiro"
SALT = b"jXuXJIUnmL2EEDCXXGjdPMOGk18rVThk"

NORMAL_COLORS = Back.BLACK + Fore.LIGHTBLUE_EX
SELECTED_COLORS = Back.LIGHTBLUE_EX + Fore.BLACK

EMPTY_ASCII_ART = {"ascii_str": "", "colors": ""}

GENSHIN_IMPACT_LINK = "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481"
ZZZ_LINK = "https://act.hoyolab.com/bbs/event/signin/zzz/e202406031448091.html?act_id=e202406031448091"
