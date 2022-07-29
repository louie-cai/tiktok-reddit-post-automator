import os
import time

from selenium.webdriver.common.by import By

from selenium import webdriver
import logging


def upload_video(driver_path: str, video_path: str, credit: str) -> None:
    logging.info(f'Uploading video {video_path}')
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=selenium')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get('https://www.tiktok.com/upload?lang=en')
    time.sleep(5)
    driver.switch_to.frame(0)
    caption = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
    caption.send_keys(
        f'{credit} #tiktok #instagram #love#viral #like #memes #follow #explorepage #trending #instagood #explore '
        f'#music #likeforlikes #funny')
    time.sleep(2)
    upload = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload.send_keys(os.path.abspath(video_path))
    time.sleep(10)
    driver.find_element(By.XPATH, '//button[@class="css-1ielthz"]').click()
    logging.info(f'Video uploaded')
    time.sleep(10)
    driver.close()