import time
import random
import os

import pytest
from utils.browser import get_mobile_browser
from utils.pop_up_handler import handle_cookies, handle_popups
from allure import step, title
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture(scope="function")
def driver():
    driver = get_mobile_browser()
    yield driver
    driver.quit()

@title("Verify")
def test_twitch_streamer_screenshot(driver):
    with step("Open browser and go to Twitch main page"):
        driver.get("https://www.twitch.tv")

    with step("Handle cookies dialog"):
        handle_cookies(driver)

    with step("Click on the search icon"):
        search_icon = driver.find_element("css selector", "a[href='/directory']")
        search_icon.click()

    with step("Input 'StarCraft II' into search field"):
        # search_box = driver.find_element("css selector", "[data-a-target='search-input']")
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-a-target='tw-input']"))
        )
        search_box.send_keys("StarCraft II")

    with step("Tap on search results with image"):
        search_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@alt='StarCraft II']/ancestor::a"))
        )
        search_result.click()


    with step("Scroll down twice"):
        for _ in range(2):
            driver.execute_script("window.scrollBy(0, 1000);")

    with step("Click on any streamer"):
        streamers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/home')]"))
        )
        # Filter visible streamers
        visible_streamers = [streamer for streamer in streamers if streamer.is_displayed()]
        random_streamer = random.choice(visible_streamers)
        # Scroll to the element (optional, for better visibility)
        driver.execute_script("arguments[0].scrollIntoView(true);", random_streamer)
        driver.execute_script("arguments[0].click();", random_streamer)

    with step("Wait until streamer's page load"):
        # wait for `follow` button on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-a-target='follow-button']"))
        )

    with step("Handle pop-up if it appears"):
        # tbh I'm not sure about this pop.
        # I didn't find any during debugging but will leave it due to requirements
        handle_popups(driver)

    with step("Take a screenshot"):
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        driver.save_screenshot("screenshots/streamer_page.png")
