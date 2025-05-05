from time import sleep

from selenium.webdriver.common.by import By

from src.shiro.config import GENSHIN_IMPACT_LINK, ZZZ_LINK
from src.checkins.selenium_utils import Driver


def submit_credentials(driver: Driver, email: str, password: str) -> None:
    try:
        login_iframe = driver.find_element_on_presence(By.ID, "hyv-account-frame")
        driver.switch_to.frame(login_iframe)
        email_field, password_field = driver.find_elements_on_presence(By.CLASS_NAME, "el-input__inner")
        driver.send_keys_to_element(email_field, email)
        driver.send_keys_to_element(password_field, password)
        login_button = driver.find_element_on_presence(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/form/button")
        driver.click_element(login_button)
        driver.switch_to.default_content()
        sleep(2)
    except Exception as exception:
        print(f"CREDENTIALS DEBUG : {exception}")


def genshin_impact_check_in(driver: Driver, email: str, password: str) -> bool:
    driver.get(GENSHIN_IMPACT_LINK)
    account_button = driver.find_element_on_presence(By.CLASS_NAME, "mhy-hoyolab-account-block")
    driver.click_element(account_button)
    submit_credentials(driver, email, password)
    load_more_button = driver.find_element_on_presence(By.XPATH, "/html/body/div[1]/div[5]/div/div/div/div[3]/span[2]")
    driver.click_element(load_more_button)
    sleep(2)
    prizes = driver.find_elements_on_presence(By.CLASS_NAME,
                                              "components-home-assets-__sign-content-test_---item-icon---3OmH_L")
    for prize in prizes:
        if driver.click_element(prize):
            return True
    return False


def zzz_check_in(driver: Driver, email, password):
    driver.get(ZZZ_LINK)
    submit_credentials(driver, email, password)
    load_more_button = driver.find_element_on_presence(By.XPATH,
                                                       "/html/body/div/div[2]/div[1]/div[4]/div/div[2]/div[2]/img")
    driver.click_element(load_more_button)
    sleep(2)
    prizes = driver.find_elements_on_presence(By.CLASS_NAME, "components-pc-assets-__prize-list_---cnt---28xt_7")
    for prize in prizes:
        if driver.click_element(prize):
            return True
    return False
