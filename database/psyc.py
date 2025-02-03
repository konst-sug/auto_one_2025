import pg8000


class PostgresDatabase:

    def __init__(self,host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        try:
            self.conn = pg8000.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise
        self.cursor = self.conn.cursor()


    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка выполнеия запроса: {e}")
            return False


    def insert_data(self, table_name, data):
        """
        Вставляет данные в указанную таблицу.

        :param table_name: Имя таблицы
        :param data: Словарь с данными для вставки
        """
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['%s']*len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders});" 
        self.execute_query(query, values)


    def disconnect(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()
            

    def __enter__(self):
        self.conn()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

