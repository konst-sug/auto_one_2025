import time
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config_data.config_test import scr_file
from .utils import auth, get_attributes

timebegin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
site_id= 'site'


def event_test(driver, logger, url_d, auth_data, test_data, save_data=False):
    '''Base psychologist test (версия для тестовых наборов) - вход в систему, переход по вкладкам кандидаты, мероприятия, создание мероприятия с выбором теста,применение 
    фильтра и расширенного фильтра поиска. При  значении переменной save_event=False запись мероприятия не происходит'''
    save_event = True if save_data > 0 else False
    try:
        logger.info('Test started at ' + timebegin)
        driver.delete_all_cookies()
        driver.get(url=url_d['t_main'])
        driver.implicitly_wait(5)
        test_status = False
        test_text = 'Test complete'
        count = 5
    except TimeoutException:
        test_text = 'Test failed: TimeExceptionError'
        logger.error("TimeoutException -  error!")
    except Exception as error:
        test_text = 'Test failed: ConnectionError'
        logger.error("Connection error")
    else:
        try:
            auth(driver, auth_data[2], auth_data[3])
            logger.info("Auth page working correct/ блок авторизации в системе - успешно!")
        except Exception as error:
            test_status = False
            test_text = 'Auth-block_form - Error'
            logger.error("Error in auth-block " + str(error))
        try:
            create_link = driver.find_element(By.LINK_TEXT, "Работники / Кандидаты")
            create_link.click()
            time.sleep(1)    
            create_link = driver.find_element(By.LINK_TEXT, "Мероприятия")
            create_link.click()
            driver.find_element(By.CSS_SELECTOR, "input[class='btn btn-success']").click()
            test_id = driver.find_element(By.ID, "id_maintest_id")
            test_id.click()
            driver.find_element(By.CSS_SELECTOR, "option[value='4']").click()
            driver.find_element(By.CSS_SELECTOR, "span[class='glyphicon glyphicon-plus']").click()
            logger.info('Event creation page - success/ Расширенный фильтр, выбор теста - успешно!')
            time.sleep(3)
        except Exception as error:
                test_status, test_text = False, 'Event creation p.1 - Error'
                logger.error("Error in event creation p.1 " + str(error))
        try:
            search_filter = 4
            form_group = driver.find_elements(By.CLASS_NAME, "form-group")
            form_group[search_filter].click()
            m_name = form_group[search_filter].find_element(By.TAG_NAME, 'input')
            #------- Поиск в расширенном фильтре по фрагменту отчества кандидата/ работника. Для изменения фильтра - изменить значение 
            # ------ номера элемента form_group: переменная search_filter 
            m_name.send_keys(test_data['search_filter_text'])
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,600)","")
            driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-success']").click()
            logger.info('Event creation full search - success/ Расширенный фильтр - успешно!')
            time.sleep(1)
        except Exception as error:
            test_status, test_text = False, "Error in event creation full search"
            logger.error("Error in event creation full search " + str(error))
        try:
            driver.execute_script("window.scrollTo(0,1200)","")   
            check = driver.find_elements(By.CLASS_NAME, "ch_employee_id")
            check[1].click()
            test_status, test_text = True, "Candidate changing - OK"
            time.sleep(1)
            if save_event:
                driver.find_element(By.CSS_SELECTOR, "button[onclick='return saveBtn();']").click()
                time.sleep(3)
                driver.save_screenshot(scr_file)
                logger.info('Event creation full - success/ Создание мероприятия - успешно!')
            else:
                logger.info('Event creation full/ Создание мероприятия - функция отключена! save_event=False')
            test_status, test_text = True, "Event creation - OK"
        except Exception as error:
            test_status, test_text = False, "Error in event creation "
            logger.error('Error in event creation ' + str(error))
        try:
            if save_event:
                modal = driver.find_element(By.CSS_SELECTOR, "div[class='modal fade in']")
                title = modal.find_element(By.CLASS_NAME, 'modal-header')
                body = modal.find_element(By.CLASS_NAME, 'modal-body').text 
                ms = title.find_element(By.TAG_NAME, "h4")
                msg = ms.find_element(By.TAG_NAME, "span")
                attrs = get_attributes(driver, msg)
                if msg.text == 'Ошибка':
                    logger.info(msg.text)
                    logger.info(body)
                else:
                    logger.info(msg.text)
                    test_status, test_text = True, "Checking event creation - OK"
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        except Exception as error:
            test_status, test_text = False, "Checking event creation - error"
            logger.error(str(error))     
    
    timer_finish = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Test finished at ' + timer_finish)

    return timebegin, site_id, test_status, test_text

