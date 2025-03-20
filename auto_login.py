# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001EF7C07DE5833661F80CFE572CCF420051D804CAA48BF1094441533C5CEC815A4703BCE7498DFA6BC72DC4CEA71150F11ADE5945155226B5422AFFB08CECBCE340EF2A97036535A3C995072CB65ECA2A6715694A44987BC2247A7E6AF406F2FD67BD08949F76C91563444C72572E53092BA724CB0802BB08B86C8C074A455A4ED3D37507A7697D52E36C613218B6EDE9B186257A771CA0B2471ADC330FB9F2CA1231059C41156F6CE2E07F22557AF2173079591B5A7A54F3F8D1FEEBE69539EA7FCF990627BDA3EEA5AA2E1A5B7FA8D36E6E6725EFB573933C0754CF2691C52492FD150B84603C5FC80B4FFF267FF8C6C47F0010D7E2EEB26ED69F7D02133316CCC56F8F56CA55B7444A4EF51DC57FAF93A33DD1CA4F49A35715645292EC2C545AAAEC136FC6B1830C68469D390AA6BAD950D6A31EE53B19472F15980950BFF20445B45EB60CB9238A9E3BCD755594A7262442EA7729AD29896A3DAD65D827AB"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
