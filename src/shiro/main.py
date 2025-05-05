from datetime import datetime
from pathlib import Path
from traceback import print_exc
from typing import Dict, List, Tuple

from src.ascii.converter import convert_image_to_ascii
from src.checkins.daily import genshin_impact_check_in, zzz_check_in
from src.shiro.config import ASCII_IMAGES_DIR, EMPTY_ASCII_ART, CHROMEDRIVER_FILE, ORIGINAL_IMAGES_FILES, SALT, \
    SERVICE_NAME, GENIUS_MOMENT_FILE, USED_PHRASES_FILE, LAST_ACTIONS_FILE, SILENT_DRIVER
from src.core.general import random_element
from src.json_utils import dump_json, overwrite_json_key
from src.core.keyring_service import KeyringService
from src.output import AsciiArt, Console, StatusBar, ConsoleObject
from src.data.parsers import parse_ascii_images, parse_kaomojis, parse_last_actions, parse_settings
from src.checkins.selenium_utils import Driver
from src.data.phrases import Phrases
from time import sleep
from telebot import TeleBot


def convert_images_to_ascii(ascii_art_settings: dict, status_bar: StatusBar) -> Dict[str, Dict[str, str]]:
    width, height, density = ascii_art_settings["width"], ascii_art_settings["lines"], ascii_art_settings["density"]
    ascii_arts = {}
    total_images = len(ORIGINAL_IMAGES_FILES)
    status_bar.update(1, None, total_images, "Converting images")
    for image_index, image_file in enumerate(ORIGINAL_IMAGES_FILES, start=1):
        status_bar.update(image_index)
        ascii_data = convert_image_to_ascii(image_file, width, height, density)
        ascii_arts[f"{image_file.stem}"] = ascii_data
        dump_json(Path(f"{ASCII_IMAGES_DIR / image_file.stem}.json"), ascii_data)
    return ascii_arts


def get_ascii_arts(ascii_art_settings: dict, sad_kaomojis: List[str], status_bar: StatusBar) -> \
        Dict[str, Dict[str, str]]:
    if ascii_art_settings["convert_on_start"]:
        ascii_arts = convert_images_to_ascii(ascii_art_settings, status_bar)
    else:
        ascii_arts = parse_ascii_images()
    return ascii_arts if ascii_arts else {f"No ascii arts found {random_element(sad_kaomojis)}": EMPTY_ASCII_ART}


def get_or_set_password(keyring_service: KeyringService, key: str, prompt: str) -> str:
    data = keyring_service.get_password(key)
    if data is None:
        data = input(f"{prompt}:")
        keyring_service.set_password(key, data)
    return data


def get_sensitive_data(user_settings: dict) -> Tuple[str, str, str, str, str]:
    master_password = user_settings["master_password"]
    if not master_password:
        master_password = input("Master password: ")
        master_password, reset = master_password.split()[0], master_password.split()[-1] in ["reset", "r"]
        if reset:
            keyring_service = KeyringService(SERVICE_NAME, master_password, SALT)
            for key in ["bot_token", "channel_id", "check_in_email", "check_in_password", "open_weather_api_key"]:
                keyring_service.delete_password(key)
            master_password = input("New master password: ")
    keyring_service = KeyringService(SERVICE_NAME, master_password, SALT)
    sensitive_keys = ["bot_token", "channel_id", "check_in_email", "check_in_password", "open_weather_api_key"]
    sensitive_data = {key: get_or_set_password(keyring_service, key, key.replace("_", " ").capitalize()) for key in
                      sensitive_keys}
    return (
        sensitive_data["bot_token"],
        sensitive_data["channel_id"],
        sensitive_data["check_in_email"],
        sensitive_data["check_in_password"],
        sensitive_data["open_weather_api_key"],
    )


def process_genius_bot(now: datetime, last_post: datetime, genius_bot_settings: dict, bot_token: str, channel_id: str,
                       sad_kaomojis: List[str], status_bar: StatusBar):
    days_past = (now - last_post).days
    upload_period_days = genius_bot_settings["post_period_days"]
    if days_past >= upload_period_days:
        phrases_to_upload = days_past // upload_period_days
        status_bar.update_with_delay(0, phrases_to_upload, f"Preparing to upload {phrases_to_upload} phrases")
        phrases = Phrases(GENIUS_MOMENT_FILE)
        used_phrases = Phrases(USED_PHRASES_FILE)
        status_bar.update_with_delay(0, None, f"Total phrases: {len(phrases)} Used phrases: {len(used_phrases)}")
        if not phrases.exclude_phrases(used_phrases):
            status_bar.update_with_delay(0, None, "Unable to exclude phrases, check .txt files")
            return
        nonexistent_author = phrases.exclude_authors(genius_bot_settings["excluded_authors"])
        if nonexistent_author is not None:
            status_bar.update_with_delay(0, None, f"{nonexistent_author} does not exist")
        random_phrases = phrases.get_random_phrases(phrases_to_upload)
        telegram_bot = TeleBot(bot_token)
        with open(USED_PHRASES_FILE, "a", encoding="utf-8") as file:
            for phrase_index, phrase in enumerate(random_phrases, start=1):
                single_line_phrase = phrase.replace("\n", " ")
                status_bar.update(phrase_index, None, None, single_line_phrase)
                telegram_bot.send_message(channel_id, phrase)
                file.write("\n" + phrase)
                sleep(genius_bot_settings["delay_between_posts_seconds"])
        overwrite_json_key(LAST_ACTIONS_FILE, "last_post", now.isoformat())
    elif genius_bot_settings["enabled"]:
        status_bar.update_with_delay(0, None, f"Not enough days past ({days_past}) {random_element(sad_kaomojis)}")


def process_check_ins(now: datetime, last_check_in: datetime, check_in_settings: dict, email: str,
                      password: str, status_bar: StatusBar) -> None:
    driver = None
    days_past = (now - last_check_in).days
    if (days_past >= 1) and check_in_settings["enabled"]:
        try:
            driver = Driver(CHROMEDRIVER_FILE, check_in_settings["driver_wait_seconds"], check_in_settings["headless"],
                            SILENT_DRIVER)
            status_bar.update_with_delay(1, 2, "Genshin impact check-in")
            if not genshin_impact_check_in(driver, email, password):
                status_bar.update_with_delay(1, None, "Prize was already collected")
            else:
                status_bar.update_with_delay(1, None, "Successfully collected prize")
            status_bar.update_with_delay(2, None, "ZZZ check-in")
            if not zzz_check_in(driver, email, password):
                status_bar.update_with_delay(2, None, "Prize was already collected")
            else:
                status_bar.update_with_delay(2, None, "Successfully collected prize")
        except Exception as selenium_exception:
            print("Selenium exception occurred during check-ins:")
            print(selenium_exception)
            input("Press any key to continue")
        finally:
            if driver is not None and driver.session_id is not None:
                driver.quit()


def main() -> None:
    # Setup
    now = datetime.now()
    user_settings, console_settings, ascii_art_settings, genius_bot_settings, check_in_settings = parse_settings()
    kaomojis = parse_kaomojis()
    last_post, last_check_in = parse_last_actions()
    bot_token, channel_id, email, password, open_weather_api_key = get_sensitive_data(user_settings)
    console = Console(console_settings)
    # TODO Replace 5 with a setting
    status_bar = StatusBar(5, 0, console)
    # Ascii arts
    ascii_arts = get_ascii_arts(ascii_art_settings, kaomojis["sad"], status_bar)
    splash_screen_name = console_settings["splash_screen_art"]
    if not splash_screen_name:
        splash_screen_name, splash_screen_data = random_element(ascii_arts)
    else:
        splash_screen_data = ascii_arts[splash_screen_name]
    splash_screen = AsciiArt(splash_screen_data, splash_screen_name, 0, 0, console)
    splash_screen.display(True, True)
    console.greet_user(now, user_settings, kaomojis["happy"], status_bar)
    # Main
    process_genius_bot(now, last_post, genius_bot_settings, bot_token, channel_id, kaomojis["sad"], status_bar)
    process_check_ins(now, last_check_in, check_in_settings, email, password, status_bar)
    status_bar.update_with_delay(1, 1, "All daily activities completed")


def debug():
    now = datetime.now()
    user_settings, console_settings, ascii_art_settings, genius_bot_settings, check_in_settings = parse_settings()
    console = Console(console_settings)
    filler = ConsoleObject([["#" * 20] * 5], 0, 0, console, None)
    filler.draw()
    console.update()
    sleep(5)
    console.clear()
    test_object = ConsoleObject(["123", "456", "789"], 1, 1, console, [[255, 0, 0], [0, 255, 0], [0, 0, 255]])
    test_object.draw()
    console.update()
    sleep(5)
    test_object.change_position(5, 5)
    test_object.draw(True)
    console.update()


if __name__ == '__main__':
    try:
        # main()
        debug()
    except Exception as exception:
        print(f"\nGeneral exception occurred: {exception}")
        print_exc()
    finally:
        input()
