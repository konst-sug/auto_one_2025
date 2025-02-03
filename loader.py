from config_data.config_maker import load_auth, load_data, load_db, load_app, load_order
from config_data.config_test import env_path, db_path_sqlite
from database.sqliter import SQLiter
from database.psyc import PostgresDatabase

auth_data = load_auth(env_path)
t_data = load_data(env_path)
db_data = load_db(env_path)
app_url = load_app(env_path)
test_list = load_order(env_path)

test_data = t_data.test
db_host = db_data.db_host
db_name = db_data.db_name
db_user = db_data.db_user
db_password = db_data.db_password
db_port = db_data.db_port
resultbase = int(db_data.resultbase)
aspt = app_url.app_url
stat = int(app_url.stat)
send = int(app_url.send)

url_d = {
        'aspt_main': aspt,
        'empl_list': f'{aspt}psychologist/employee/list.html',
        'psyc_list': f'{aspt}psychologist/event/list.html',
        'event_create': f'{aspt}psychologist/event/create.html',
        'report_page': f'{aspt}psychologist/report/list.html',
        'aspt_admin': f'{aspt}admin/user/list.html',
        'admin_create': f'{aspt}admin/user/create.html',
        'report1': f'{aspt}psychologist/report/report_event.html',
        'report2': f'{aspt}psychologist/report/report_testing.html',
        'report3': f'{aspt}psychologist/report/report_mark.html',
        'report4': f'{aspt}psychologist/report/report_candidate.html'
        }

if resultbase:
    db = PostgresDatabase(db_host, db_port, db_name, db_user, db_password)
else:
    db = SQLiter(db_path_sqlite)
#------------------test list for starter\tester ----------------------------
#test_list = [21,22,11]
#------------------test list for cron -------------------------------
#cron_test_list = [40,20,11,30,50,32,13]
cron_test_list = [11]

# ----------------functions_to_test_list-----------------------------
# ----------------add number for testsuite in test_list -------------
#     11: "admin_test"--  Base admin test - вход в систему, переход по вкладкам справочники, пользователи, создание пользователя,применение фильтра.'
#     21: "event_test"--  Base psychologist test - вход в систему, переход по вкладкам кандидаты, мероприятия, создание мероприятия с выбором теста,применение фильтра и расширенного фильтра поиска.
#     22: "emp_create"--  Second psychologist test - вход в систему, переход на вкладку кандидаты, создание кандидата, проверка сохранения записи при помощи поиска по фильтру. 
#                         По умолчанию производится запись в БД, для отключения переменной save_rec присвоить значение False (0)
#     23: "report_test"-- Psychologist report test (версия для тестовых наборов) - вход в систему, переход на вкладку отчеты, создание четырех видов отчетов, 
#                         применение фильтра и расширенного фильтра поиска. Переменная report_type задает вид проверяемого отчета, принимает значения: 0-3
#     32: ""      -- 
#     33: ""      -- 
#     40: ""      -- 
#     41: ""      -- 
#     42: ""       -- 

#--------- path to image to upload, file name to screenshot----------
foto_url = '/home/user/Изображения/cat_eyes.png'
