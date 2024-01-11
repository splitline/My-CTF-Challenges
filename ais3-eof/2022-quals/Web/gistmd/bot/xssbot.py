#!/usr/bin/env python3
import time
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

TIMEOUT = 5


def browse(note_id):
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome = Chrome(options=options)
    chrome.set_page_load_timeout(TIMEOUT)
    chrome.set_script_timeout(TIMEOUT)

    try:
        # login
        base_url = 'http://web'
        username, password = 'administrator', os.getenv('ADMIN_PASSWORD')

        chrome.get(base_url + "/login")
        chrome.find_element_by_name('username').send_keys(username)
        chrome.find_element_by_name('password').send_keys(password)
        chrome.find_element_by_css_selector('input[type="submit"]').click()

        # visit
        chrome.get(base_url + "/note/" + note_id)
        time.sleep(TIMEOUT)
    except (TimeoutException, WebDriverException) as e:
        print(e)
    finally:
        chrome.quit()
