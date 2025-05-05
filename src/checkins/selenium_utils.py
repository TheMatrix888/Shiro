from typing import List, Optional

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException, InvalidSelectorException, JavascriptException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import ByType
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Driver(Chrome):
    def __init__(self, chromedriver_path: str, webdriver_wait_seconds: int, headless: bool, silent: bool):
        self.webdriver_wait_timeout_seconds = webdriver_wait_seconds
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-agent={UserAgent.chrome}')
        if headless:
            options.add_argument("--headless=new")
        else:
            options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_experimental_option("detach", False)
        log_path = "NUL" if silent else None
        service = Service(executable_path=chromedriver_path, log_path=log_path)
        super().__init__(options, service)

    def find_element_on_presence(self, by: ByType, value: str) -> Optional[webelement]:
        try:
            WebDriverWait(self, self.webdriver_wait_timeout_seconds).until(
                expected_conditions.presence_of_element_located((by, value)))
            element = self.find_element(by, value)
            return element
        except (TimeoutException, InvalidSelectorException):
            return None

    def find_elements_on_presence(self, by: ByType, value: str) -> Optional[List[webelement]]:
        try:
            WebDriverWait(self, self.webdriver_wait_timeout_seconds).until(
                expected_conditions.presence_of_element_located((by, value)))
            elements = self.find_elements(by, value)
            return elements
        except (TimeoutException, InvalidSelectorException):
            return None

    def focus_element(self, element: webelement):
        try:
            self.execute_script("arguments[0].scrollIntoView();", element)
            return True
        except (InvalidSelectorException, JavascriptException):
            return False

    def click_element(self, element: webelement) -> bool:
        try:
            if not self.focus_element(element):
                return False
            element.click()
            return True
        except ElementClickInterceptedException:
            return False

    def send_keys_to_element(self, element: webelement, text: str) -> bool:
        if not self.focus_element(element):
            return False
        element.send_keys(text)
        return True
