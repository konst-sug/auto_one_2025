import datetime
import logging
import time

from config_data.config_test import  chrome_options, functions_in_acc, test_log
from functions import *
from loader import test_list, test_data, auth_data, resultbase, db, url_d, stat, send
from selenium import webdriver


logging.basicConfig(level=logging.INFO)
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(30)
timer = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(test_log)


#-------------------format & save data to database ------------------
def db_saver(data: list, func: str):
    '''--- Запись в БД в зависимости от настройки в файле окружения: переменная resultbase'''
    if resultbase:
        # ---- Для записи в постгрес данные необходимо преобразовать в словарь ----
        data_dict = {}
        data_dict['done_time'] = data[0]
        data_dict['site_id'] = data[1]
        data_dict['module_name'] = func
        data_dict['test_status'] = data[2]
        data_dict['descr'] = data[3]
        logger.info("Запись ведется в базу PostgreSQL")
        db.insert_data("result_table", data_dict)
    else:
        # ---- Запись в БД SQLite -----
        logger.info("Запись ведется в базу SQLite!")
        db.post_info("result_table", data[0],data[1], func, data[2], data[3])  


def order_tests(send=False, stat=False, tests=test_list):
    '''send -- сохранение пользователей/кандидатов/ мероприятий, по умолчанию - False; для функции по проверке формирования отчетов для психолога 
       может принимать значения для выбота типа отчета (от 0 до 3); для остальных тестов True/False (0/1)
       stat -- запись результата в БД, по умолчанию - False;
       tests -- список номеров тестовых сценариев, по умолчанию загружается из loader; '''
    time_begin = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for i in tests:
        try:
            func = functions_in_acc[i]
            driver.delete_all_cookies()
            res = globals()[func](driver, logger, url_d, auth_data, test_data, send)
        except Exception as error:
            logger.error("Error on Order tests")
            res = [time_begin, 'aspt', False, "Error on Order tests"]
        time.sleep(1)
        if stat:
            db_saver(res, func) 
        logging.info(f'{time_begin}--{i}--{func}')
    driver.close()    

        
def main():
    order_tests(send, stat)
    

if __name__ == '__main__':
    main()
