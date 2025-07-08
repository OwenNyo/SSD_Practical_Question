from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- CONFIG ---
BASE_URL = "http://localhost:5000"
CHROME_PATH = os.getenv("CHROME_BIN", "/usr/bin/google-chrome-stable")

# --- SETUP ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = CHROME_PATH
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

def test_password(input_pw, should_pass=True):
    try:
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "password")))

        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(input_pw)

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        current_url = driver.current_url
        page_source = driver.page_source.lower()

        if should_pass:
            assert "welcome" in current_url.lower(), f"❌ Expected redirect, got {current_url}"
            assert "your password:" in page_source, "❌ Missing welcome message."
            print(f"✅ Passed test with VALID password: '{input_pw}'")
        else:
            assert "welcome" not in current_url.lower(), "❌ Redirected despite INVALID password"
            assert "invalid password" in page_source, "❌ Missing error message for invalid password."
            print(f"✅ Passed test with INVALID password: '{input_pw}'")
    except Exception as e:
        print(f"❌ Error testing password '{input_pw}':", e)

# --- RUN TESTS ---
test_password("Valid123!", should_pass=True)
test_password("bad", should_pass=False)

driver.quit()
