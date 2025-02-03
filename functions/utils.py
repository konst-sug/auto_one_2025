import datetime
from selenium.webdriver.common.by import By
import time


def auth(driver, log, password) -> None:
    login = driver.find_element(By.ID, "j_login")
    psw = driver.find_element(By.CSS_SELECTOR, "input[name='j_password']")
    submit = driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-primary']")
    login.send_keys(log) 
    psw.send_keys(password)
    submit.click()


def change_report(driver, repo_number: int) -> None:
    """repo_ number - номер отчета на странице, сверху вниз начиная с 0"""
    row = driver.find_element(By.CLASS_NAME, 'row')
    row = driver.find_element(By.CLASS_NAME, 'theme-content-layer')
    time.sleep(1)
    links = row.find_elements(By.CSS_SELECTOR, "a")
    links[repo_number].click()


def set_date(driver, frmdate: str, todate: str) -> None:
    '''Set date range for reports - задать диапазон дат для построения отчетов. '''
    form_group = driver.find_elements(By.CLASS_NAME, "form-group")
    form_group[0].click()
    m_name = form_group[0].find_element(By.TAG_NAME, 'input')
    m_name.send_keys(frmdate)
    time.sleep(1)
    form_group[1].click()
    m_name = form_group[1].find_element(By.TAG_NAME, 'input')
    m_name.send_keys(todate)


def get_count(driver, logger, search_text: str) -> int:
    '''Поиск количества записей по фильтру '''
    search_count = ''
    try:
        driver.find_element(By.CSS_SELECTOR, "input[type='search']").send_keys(search_text)
        driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-search btn-my-search']").click()
        res = driver.find_element(By.CSS_SELECTOR, "div[class='dataTables_info']").text
        search_count = int(res[13:16:])      
        logger.info("Checking count of records - sucsess! / поиск количества записей по фильтру")
        logger.info(res)
    except Exception as error:
        logger.error("Error in checking count of records " + str(error))
    return search_count


def get_attributes(driver, element) -> dict:
    return driver.execute_script(
        """
        let attr = arguments[0].attributes;
        let items = {}; 
        for (let i = 0; i < attr.length; i++) {
            items[attr[i].name] = attr[i].value;
        }
        return items;
        """,
        element
    )