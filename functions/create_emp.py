import datetime
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config_data.config_test import scr_file
from .utils import auth

timebegin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
site_id= 'site'


def get_count(driver, logger, url, search_text: str) -> int:
    '''Поиск количества записей по фильтру '''
    search_count = 0
    try:
        driver.get(url=url)
        driver.implicitly_wait(5)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "input[type='search']").send_keys(search_text)
        driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-search btn-my-search']").click()
        res = driver.find_element(By.CSS_SELECTOR, "div[class='dataTables_info']").text
        search_count = int(res[13:16:])      
        logger.info("Checking count of records - sucsess! / поиск количества записей по фильтру")
        logger.info(res)
    except Exception as error:
        logger.error("Error in checking count of records " + str(error))
    return search_count


def emp_create(driver, logger, url_d, auth_data, test_data, save_data = False):
    '''Second psychologist test (версия для тестовых наборов) - вход в систему, переход на вкладку кандидаты, создание кандидата,
    проверка сохранения записи при помощи поиска по фильтру. По умолчанию производится запись в БД, для отключения
    переменной save_rec присвоить значение False (0)'''
    save_rec = True if save_data > 0 else False
    try:
        driver.get(url=url_d['t_main'])
        url = url_d['empl_list']
        driver.implicitly_wait(5)
        logger.info('Test started at ' + timebegin)
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        test_status = True
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
            auth(driver, auth_data[2], auth_data[3])
            time.sleep(3)
            count = get_count(driver, logger, url, test_data['search_text'])
            logger.info("Auth page working correct/ блок авторизации в системе - успешно!")
            logger.info(f"Количество записей по фильтру {count}")
        except Exception as error:
            test_status = False
            test_text = 'Auth-block_form - Error'
            logger.error("Error in auth-block" + str(error))
        try:
            create_link = driver.find_element(By.LINK_TEXT, "Работники / Кандидаты")
            create_link.click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[class='btn btn-success']").click()
            logger.info("link to createion candidate correct/ блок перехода к созданию кандидата - успешно!")
        except Exception as error:
            test_status = False
            test_text = 'Error in link to createion candidate'
            logger.error("Error in link to createion candidate " + str(error))
        try:
            dep_id = driver.find_element(By.ID, "id_department_id")
            driver.find_element(By.CSS_SELECTOR, "button[class='ct-arrow-btn']").click()
            time.sleep(1)
            dep_id.send_keys("ЛВЧД")
            dep_id = driver.find_element(By.CSS_SELECTOR, "span[data-id='39']")
            dep_id.click()
            time.sleep(2)
            logger.info("OHS search working correct/ поиск по ОШС - успешно!" )
            driver.find_element(By.CSS_SELECTOR, "button[class='ct-arrow-btn']").click()
            l_name = driver.find_element(By.ID, "id_last_name")
            name = driver.find_element(By.ID, "id_first_name")
            m_name = driver.find_element(By.ID, "id_middle_name")
            l_name.send_keys(test_data['last_name'])
            name.send_keys(test_data['name'])
            m_name.send_keys(test_data['middle_name'])
            driver.find_element(By.CSS_SELECTOR, "input[value='2']").click()
            time.sleep(1)
        except Exception as error:
            test_status = False
            test_text = 'Error in create candidate part 1 '
            logger.error("Error in create candidate part 1 " + str(error))
        try:    
            b_date = driver.find_element(By.ID, "id_birth_date")
            b_date.click()
            create_link = driver.find_element(By.LINK_TEXT, "1")
            create_link.click()
            time.sleep(.5)
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            b_date.clear()
            b_date.send_keys(test_data['birth_date'])
            driver.find_element(By.CSS_SELECTOR, "button[data-id='id_position_id']").click()
            time.sleep(.8)
            driver.find_element(By.CSS_SELECTOR, "input[type='search']").send_keys("Кас")
            logger.info("search field available, working correct")
            time.sleep(.8)
            driver.find_element(By.ID, "bs-select-1-0").click()
            driver.find_element(By.ID, "id_email").send_keys(test_data['mail'])
            time.sleep(.8)
            if save_rec:
                driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-success']").click()
            time.sleep(3)
            logger.info("create candidate part 2 working correct/ создание аккаунта кандидата - успешно!" )
            driver.save_screenshot(scr_file)
        except Exception as error:
            test_status = False
            test_text = 'Error in create candidate part 2'
            logger.info("Error in create candidate part 2 " + str(error))
        try:
            final_count = get_count(driver, logger, url, test_data['last_name'])
            time.sleep(3)
            if final_count > count:
                logger.info("checking creation candidate/ кандидат успешно сохранен!")
            else:
                logger.error("Error saving the new record/ ошибка сохранения кандидата/ переменная save_rec=" + str(save_rec) )
                test_status = False
                test_text = 'Error saving the new record'
        except Exception as error:
            logger.error("Error in check for creation candidate " + str(error))
    
    timer_finish = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Test finished at ' + timer_finish)
    return timebegin, site_id, test_status, test_text
