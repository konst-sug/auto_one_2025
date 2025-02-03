import time
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config_data.config_test import  scr_file
from .utils import auth, get_count

timebegin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
site_id= 'site'


def send_data(form_group,auth_data, inp_number: int):
    form_group[inp_number].click()
    form = form_group[inp_number].find_element(By.TAG_NAME, 'input')
    form.send_keys(auth_data[inp_number+2])


def admin_test(driver, logger, url_d, auth_data, test_data, save_data=False):
    '''Base admin test - вход в систему, переход по вкладкам справочники, пользователи, создание пользователя,
    применение фильтра.'''
    save_user = True if save_data > 0 else False
    try:
        logger.info('Test started at ' + timebegin)
        driver.get(url=url_d['t_main'])
        driver.implicitly_wait(5)
        test_status = False
        test_text = 'Test complete'
    except TimeoutException:
        test_text = 'Test failed: TimeExceptionError'
        logger.error("TimeoutException -  error!")
        driver.close()
    except Exception as error:
        test_text = 'Test failed: ConnectionError'
        logger.error("Connection error")
        driver.close()
    else:
        try:
            auth(driver, auth_data[0], auth_data[1])
            logger.info("Auth page working correct/ блок авторизации в системе - успешно!")
            test_status = True
        except Exception as error:
            test_status = False
            test_text = 'Auth-block_form - Error'
            logger.error("Error in auth-block " + str(error))
        try:
            creation_link = driver.find_element(By.LINK_TEXT, "Справочники")
            creation_link.click()
            time.sleep(1)    
            creation_link = driver.find_element(By.LINK_TEXT, "Пользователи")
            creation_link.click()
            driver.find_element(By.CSS_SELECTOR, "input[class='btn btn-success']").click()
            logger.info("Link to user creation page - success!/ Переход на страницу создания пользователя.")
            time.sleep(1)
        except Exception as error:
                test_status, test_text = False, 'Link to user creation - Error'
                logger.error("Error in link to user creation page" + str(error))
        try:
            user_type = 1
            form_group = driver.find_elements(By.CLASS_NAME, "form-group")
            time.sleep(1) 
            form = form_group[0].find_elements(By.TAG_NAME, 'input')
            form[user_type].click()
            time.sleep(1)        
            logger.info("Type of user choosed/ Выбор типа пользователя - успешно!")
        except Exception as error:
            test_status, test_text = False, 'Unable to change type of user'
            logger.error("Unable to change type of user")
        try:
            #----change department/ выбор структурного подразделения--------
            form_group[1].click()
            form = form_group[1].find_element(By.TAG_NAME, 'input')
            form.click()
            form_group[1].find_element(By.CSS_SELECTOR, 'span[data-id="1"]').click()
            driver.execute_script("window.scrollTo(0,400)","")
            time.sleep(1)
            #----data entry/ ввод данных нового пользователя---------------
            for i in range(2,7):
                send_data(form_group,auth_data, i)
                time.sleep(.5)
            driver.execute_script("window.scrollTo(0,500)","")
            form = form_group[7].find_elements(By.TAG_NAME, 'input')
            form[1].click()
            logger.info('User creation form record - success/ Внесение данных пользователя ч.1 - успешно!')
            time.sleep(1)
        except Exception as error:
            test_status, test_text = False, "Error in creation form record p.1 - Error"
            logger.error("Error in creation form record p.1 " + str(error))
        try:
            send_data(form_group, auth_data, 8)
            if save_user:
                driver.find_element(By.CSS_SELECTOR, "button[onclick='return saveBtn();']").click()
            time.sleep(3)
            logger.info('User creation full - success/ Создание пользователя - успешно! Значение save_user=' + str(save_user))
            test_status = True
        except Exception as error:
            test_status, test_text = False, "Error in user creation!"
            logger.error('Error in user creation ' + str(error))
        try:
            driver.get(url=url_d['aspt_admin'])
            time.sleep(2)  
            get_count(driver, logger, auth_data[4])
            driver.save_screenshot(scr_file)
        except Exception as error:
            logger.error('Error in check user creation')
   
    timer_finish = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Test finished at ' + timer_finish)
    return timebegin, site_id, test_status, test_text
