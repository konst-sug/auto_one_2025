from dataclasses import dataclass
from environs import Env


@dataclass
class AuthData:
    auth_data: list[int]


@dataclass
class TestData:
    test: list[str]


@dataclass
class OrderTest:
    ordertest: list[int]


@dataclass
class DatabaseConfig:
    db_name: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных 
    db_port: str              
    resultbase: int       # Тип БД для сохранения


@dataclass
class AppConfig:
    app_url: str        # базовый url для доступа к приложению
    stat: bool           # переменная для статуса записи в БД (0-запись не ведется/ 1-запись ведется)
    send: int           # переменная для статуса создания объектов в системе (0-не сохранять/ 1-сохранять, в случае теста отчетов номер отчета для создания)


def load_data(path: str | None= None) -> TestData:
    env = Env()
    env.read_env(path)
    return TestData(test=env.dict('TESTDATA'))


def load_app(path: str | None= None) -> AppConfig:
    env = Env()
    env.read_env(path)
    return AppConfig(app_url=env('APP_URL'),    
                    stat=env('STAT'),
                    send=env('SEND'))


def load_auth(path: str | None= None) -> AuthData:
    env = Env()
    env.read_env(path)
    auth_data=list(map(str,env.list('AUTH')))
    return auth_data


def load_order(path: str | None= None) -> OrderTest:
    env = Env()
    env.read_env(path)
    order_data=list(map(int,env.list('TEST_LIST')))
    return order_data


def load_db(path: str | None= None) -> DatabaseConfig:
    env = Env() 
    env.read_env(path)
    return DatabaseConfig(db_host=env('DB_HOST'),
                    db_name=env('DB_NAME'),
                    db_user=env('DB_USER'),
                    db_password=env('DB_PASSWORD'),
                    db_port=env('DB_PORT'),
                    resultbase=env('RESULTBASE'))