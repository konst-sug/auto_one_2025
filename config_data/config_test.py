from fake_useragent import UserAgent
import logging
from log_filters import TestLogFilter
from selenium.webdriver.chrome.options import Options
import pathlib

ua = UserAgent()
ua_ag = ua.random
chrome_options = Options()
chrome_options.add_argument(f'user-agent={ua_ag}')
prefs = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--zoom=0.8")
chrome_options.page_load_strategy = "eager"  #---'normal', 'eager', 'none'
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# ------------ test phone to upload ----------------------------------
test_phone = +79180000001

#--------- logging settings  -----------------------------------------
formatter_1 = logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d :%(funcName)s - %(message)s'
)

test_log = logging.FileHandler('results/test.log', 'a', encoding='utf-8')
test_log.setLevel(logging.DEBUG)
test_log.addFilter(TestLogFilter())
test_log.setFormatter(formatter_1)

#---------get the working directory path, db path, upload path ------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
path = pathlib.PosixPath(BASE_DIR)
index = path.parts.index('app')
project_dir = pathlib.PurePosixPath(*path.parts[:index+1])
db_path_sqlite = project_dir.joinpath('database/result.db')
target_folder = project_dir.joinpath('results')
env_path = project_dir.joinpath('env')

print(BASE_DIR, db_path_sqlite, sep='\n')
print(env_path, target_folder, sep="\n")

# -------  time pause for tests  ------------------------------------
time_pause1 = 1
time_pause2 = 3

functions_in_acc = {
    11: "admin_test",
    21: "event_test",
    22: "emp_create",
    23: "report_test",
    32: "",
    33: "", 
    40: "",
    41: "",
    42: ""
}

# ------------ test data to upload -----------------------
test_data = {
        'frmdate': '22.02.2022',
        'todate': '22.02.2024',
        'last_name': 'Тестова',
        'name': 'Мария',
        'middle_name': 'Сбитеховна',
        'birth_date': '20.04.2001',
        'mail': 'testmail@mail.ru',
        'search_text': 'Тестова',
        'search_filter_text': 'петр'
        }

#--------- file name to screenshot ------------------------
scr_file = 'screen1.png'

