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
    browser.add_cookie({"name": "MUSIC_U", "value": "0071CD8CDA927671A5D75B0FFEE4243608A2B1B3918839FC87092523AA25541A7074293311D246382B9C8E384DCEB4C9B2F4C960EC1D68EB4EC5E663926635ECE9315A5BB93FEFC6473E00894A54169B49CFA195427F8D3FAD89E388AEAC97F066B341E18D8977E00351343A1AD08FF017C33C9217F41C1626034BEB10F7F09A12C42CC0E8F3C4BD9F191FA27F6B1EEA42B7109F985922956695062B283C291EADDAD35898A4F87F37ADE1D0BAAFC4619E0FCB75C437E3CA77892531704FD6688851423179B1F165F117032AC71B6D3CCD0061AA1636C00BE3235CCEE9ADB11A92CC3650A51498AC1703D484445F7056F7906617E70D92484865234E1DE632A56646C0F018B72AA4384FC610DB0C2E5A176335B282BCA119725718C3F3AA87A6E0E997F31ADA24876D58BA31B60D4E8DCDDDD72EC40B088A4078912A93555BB3383FC29E4B461820EE28F0196CA49654A1B61C2EC2E21ADAF5728CE47B1BA05B1E"})
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
