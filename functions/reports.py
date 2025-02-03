
import time
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config_data.config_test import scr_file
from .utils import auth, get_count, set_date, change_report

timebegin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
site_id= 'site'


def report_test(driver, logger, url_d, auth_data, test_data, report_type=0):
    '''Psychologist report test (версия для тестовых наборов) - вход в систему, переход на вкладку отчеты, создание четырех видов отчетов,
    применение фильтра и расширенного фильтра поиска. Переменная report_type задает вид проверяемого отчета, принимает значения: 0-3'''
    try:
        logger.info('Test started at ' + timebegin)   
        driver.get(url=url_d['t_main'])
        driver.implicitly_wait(5)
        test_status = False
        test_text = 'Test complete'
    except TimeoutException:
        test_text = 'Test failed: TimeExceptionError'
        logger.error("TimeoutException -  error!")
    except Exception as error:
        test_text = 'Test failed: ConnectionError'
        logger.error("Connection error")
    else:
        try:
            auth(driver, auth_data[2], auth_data[3])
            test_status = True
            logger.info("Auth page working correct/ блок авторизации в системе - успешно!")
        except Exception as error:
            test_status = False
            test_text = 'Auth-block_form - Error'
            logger.error("Error in auth-block " + str(error))
        try:
            create_link = driver.find_element(By.LINK_TEXT, "Отчеты")
            create_link.click()
            time.sleep(1)  
            change_report(driver, report_type)
            time.sleep(1)
            logger.info("reports page working correct/ блок отчетов психолога - успешно!")
        except Exception as error:
            test_status = False
            test_text = 'change report-block - Error'
            logger.error("Error in change report-block " + str(error))      
        try:
            set_date(driver, test_data['frmdate'], test_data['todate'])
            driver.execute_script("window.scrollTo(0,400)","")
            time.sleep(1)
            logger.info("reports creation page  working correct/ формирование отчета  - успешно!")
        except Exception as error:
            test_status = False
            test_text = 'change report-block - Error'
            logger.error("Error in change report-block " + str(error))
        try:     
            driver.find_element(By.CSS_SELECTOR, "button[onclick='return executeBtn();']").click() 
            time.sleep(5)
            driver.execute_script("window.scrollTo(0,600)","")
            ex_link = driver.find_element(By.ID, 'id_report_excel')
            table = driver.find_element(By.ID, 'id_report_data')
            records = table.find_elements(By.TAG_NAME, 'tr')
            logger.info("Report created/ Excel link is enabled " + str(ex_link.is_enabled()))
            logger.info("Report created/ Table is displayed " + str(table.is_displayed()))
            logger.info("Report created/ Count of records "+ str(len(records)))
            time.sleep(1)
        except Exception as error:
            test_text = 'make report-block - Error'
            logger.error("Error in report creation block " + str(error))        
   
    timer_finish = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Test finished at ' + timer_finish)

    return timebegin, site_id, test_status, test_text 
