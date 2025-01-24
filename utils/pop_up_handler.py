from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_popups(driver):
    try:
        close_button = driver.find_element("css selector", "[aria-label='Close']")
        close_button.click()
    except Exception:
        pass  # If no popup is present, continue

def handle_cookies(driver):
    try:
        # Wait for the cookie banner to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-a-target='consent-banner-accept']"))
        )
        # Click the "Accept Cookies" button
        accept_button = driver.find_element(By.CSS_SELECTOR, "[data-a-target='consent-banner-accept']")
        accept_button.click()
        print()
    except Exception as e:
        print(f"No cookie banner displayed or failed to close it: {e}")