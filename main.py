from math import floor

import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = '/Users/cheza/Drivers/chromedriver'
driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path))

driver.get('https://orteil.dashnet.org/cookieclicker/')

current_max = 0


def load_page():
    try:
        english_select = driver.find_element(by=By.CSS_SELECTOR, value='#langSelect-EN')
        english_select.click()
    except NoSuchElementException:
        load_page()


def check_points() -> str:
    try:
        cookie = driver.find_element(by=By.CSS_SELECTOR, value='#cookies')
        return cookie.text
    except StaleElementReferenceException:
        print('Unable to find element')
        check_points()


def click_button():
    try:
        cookie_button = driver.find_element(by=By.CSS_SELECTOR, value='#cookieAnchor').find_element(by=By.TAG_NAME,
                                                                                                    value='button')
        cookie_button.click()
    except StaleElementReferenceException:
        print('Cannot find button')
        click_button()


def check_products():
    global current_max
    product_content = driver.find_elements(by=By.CSS_SELECTOR, value='.unlocked')
    count = len(product_content)
    for i in range(0, count):
        try:
            product_price = float(
                driver.find_element(by=By.CSS_SELECTOR, value=f'#productPrice{i}').text.replace(',', ''))
            if product_price >= current_max:
                product_content[i].click()
                current_max = product_price
        except ValueError as ex:
            print(f'Value error {ex}')


load_page()
timeout = time.time() + 60 * 5
elapsed_time = time.time()
start_time = time.time()
while time.time() < timeout:
    click_button()
    elapsed_time = floor(time.time() - start_time)
    if elapsed_time % 5 == 0:
        check_products()

print(check_points())
