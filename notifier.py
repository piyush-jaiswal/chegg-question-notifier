import logging
import os
import pickle
import random
import time

from dotenv import load_dotenv
from plyer import notification
from pyshadow.main import Shadow
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_cookie_path():
    return os.path.join(os.getenv("COOKIES_DIR"), "cookies.pkl")


def login_and_save_cookie():
    logging.info("Logging in")

    driver = webdriver.Chrome(os.getenv("CHROMEDRIVER_PATH"))
    driver.get('https://expert.chegg.com')

    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    time.sleep(random.uniform(3, 6))
    username.send_keys(os.getenv("EMAIL"))
    time.sleep(0.5)
    username.send_keys(Keys.RETURN)

    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    time.sleep(random.uniform(3, 6))
    password.send_keys(os.getenv("PASSWORD"))
    time.sleep(0.5)
    password.send_keys(Keys.RETURN)

    try:
        qna = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="expert-qna-button"]')))
        time.sleep(random.uniform(1, 2))
        qna.click()
        time.sleep(10)
    except TimeoutException:
        logging.exception("Could not locate 'expert-qna-button'")
    finally:
        logging.info("Saving Cookies")
        pickle.dump(driver.get_cookies(), open(get_cookie_path(), "wb"))
        driver.close()


def hard_refresh(driver):
    logging.info('Hard refreshing')

    if len(driver.window_handles) == 1:
        driver.execute_script("window.open('')")  # Create a separate tab than the main one

    driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
    driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.

    time.sleep(0.5)
    shadow = Shadow(driver)
    browsing = shadow.find_element("settings-checkbox[id='browsingCheckboxBasic']")
    if browsing.get_attribute('checked'):
        browsing.click()
    cookies = shadow.find_element("settings-checkbox[id='cookiesCheckboxBasic']")
    if cookies.get_attribute('checked'):
        cookies.click()
    shadow.find_element("cr-button[id='clearButton']").click()

    time.sleep(2)

    # Switch Selenium controls to the original tab to continue normal functionality.
    driver.switch_to.window(driver.window_handles[0])

    driver.refresh()


def check_for_question():
    logging.info("Checking for question")

    driver = webdriver.Chrome(os.getenv("CHROMEDRIVER_PATH"))
    driver.get('https://expert.chegg.com')
    cookies = pickle.load(open(get_cookie_path(), "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    try:
        driver.get('https://expert.chegg.com/qna/authoring/answer')
        while True:
            try:
                no_ques = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="no-question"]')))
                if no_ques.is_displayed():
                    time.sleep(random.uniform(10, 20))
                    hard_refresh(driver)

            except TimeoutException:
                notification.notify(title="Chegg", message="Found question", app_icon=None, timeout=10)
                logging.info('Found question')
                input("Press any key to continue.")

    except Exception:
        logging.exception("Found exception")


def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    login_and_save_cookie()
    check_for_question()


if __name__ == '__main__':
    main()
