from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import random

# --- CONFIGURATION ---
CHROME_DRIVER_PATH = r"D:\DOWNLOADS\chromedriver-win64\chromedriver-win64\chromedriver.exe"
CSV_PATH = r"D:\DOWNLOADS\zomato_profiles.csv"  # CSV should have a column named 'profile_url'

# --- Setup Chrome ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 10)

def wait_for_manual_login():
    print("Opening Zomato... please log in manually.")
    driver.get("https://www.zomato.com/login")
    input("🔐 After logging in, press ENTER to continue...")

def follow_user(profile_url):
    try:
        print(f"Visiting {profile_url}")
        driver.get(profile_url)
        time.sleep(random.uniform(2, 4))  # Let page render JS

        # Try finding the button using XPath
        follow_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Follow"]/ancestor::button'))
        )
        follow_button.click()
        print(f"✅ Followed: {profile_url}")
        time.sleep(random.uniform(2, 5))
        return True

    except TimeoutException:
        print(f"❌ Follow button not found or not clickable on {profile_url}")
    except Exception as e:
        print(f"⚠️ Error on {profile_url}: {e}")
    return False

def main():
    wait_for_manual_login()

    df = pd.read_csv(CSV_PATH)
    results = []

    for idx, row in df.iterrows():
        profile_url = row.get("profile_url")
        if profile_url:
            success = follow_user(profile_url)
            results.append((profile_url, success))

    pd.DataFrame(results, columns=["profile_url", "followed"]).to_csv("follow_results.csv", index=False)
    print("🎯 All done. Results saved to follow_results.csv.")
    driver.quit()

if __name__ == "__main__":
    main()
