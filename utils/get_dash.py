from time import sleep
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from config_data.config_one_test import update_path
from utils import get_settings



def dashboard_shot(driver):
    print("!!!!")
    try:
        driver.get("http://localhost:3000/d/")
        driver.implicitly_wait(10)
        driver.delete_all_cookies()
        sleep(1)
        frame = driver.find_element(By.CSS_SELECTOR, 'div[class="login-content-box css-odanoj"]')
        logging.info(f'submit button {frame.is_enabled()}')
        sleep(1)
        user = frame.find_element(By.CSS_SELECTOR, "input[name='user']")
        user.send_keys('admin')
        sleep(1)
        frame.find_element(By.CSS_SELECTOR,"button[class='css-1c5twjv-button']").click()
        frame.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys("admin")
        sleep(1)
        frame.find_element(By.CSS_SELECTOR,"button[class='css-1c5twjv-button']").click()
        
        timer, res_file = get_settings(update_path)
        print(timer)
        frame.find_element(By.CSS_SELECTOR, "button[class='css-bhnz0e-button'] ").click()
        driver.find_element(By.CSS_SELECTOR, "a[class='css-1nqqpiv']").click()
        sleep(1)
        driver.get(url='http://localhost:3000/d/')
        sleep(2)
        driver.save_screenshot(res_file)
        
    except Exception as error:
        logging.error('Error in Grafana screenshot'+ str(error))    
    return timer, res_file
