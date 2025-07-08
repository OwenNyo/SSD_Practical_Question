from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use GitHub Actions environment variable (set in workflow)
    chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/google-chrome-stable")
    options.binary_location = chrome_bin

    # Point to chromedriver installed by apt
    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)

def test_valid_password():
    driver = setup_driver()
    try:
        driver.get("http://127.0.0.1:5000")

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("Valid123!")

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        assert "welcome" in driver.current_url.lower(), "❌ Did not redirect to welcome page for valid password"
        assert "Your password:" in driver.page_source, "❌ Welcome message missing for valid password"

        print("✅ Valid password test passed.")
    finally:
        driver.quit()

def test_invalid_password():
    driver = setup_driver()
    try:
        driver.get("http://127.0.0.1:5000")

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("bad")  # too short, lacks requirements

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        assert "welcome" not in driver.current_url.lower(), "❌ Redirected with invalid password"
        assert "Invalid password." in driver.page_source, "❌ Missing error message for invalid password"

        print("✅ Invalid password test passed.")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_valid_password()
    test_invalid_password()
