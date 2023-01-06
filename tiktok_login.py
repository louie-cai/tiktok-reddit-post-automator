from selenium import webdriver
import time

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=selenium")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    driver.get("https://www.tiktok.com/upload?lang=en")
    time.sleep(1000000)
