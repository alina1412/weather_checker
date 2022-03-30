import sqlite3


class DatabaseEditor:
    def __init__(self):
        self.d_name = "last_weather.db"
        self.connect = None
        self.make_connection()
        self.main_creating_query = """CREATE TABLE IF not EXISTS weather (
        n_id INTEGER PRIMARY KEY
        , city varchar(255)
        , weather int
        )
        """
        self.create_main_db()

    def close(self):
        if self.connect:
            self.connect.close()

    def make_connection(self):
        try:
            connect = sqlite3.connect(self.d_name)
            self.connect = connect
        except sqlite3.Error as error:
            print(error)

    def create_table(self, query):
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(query)
            self.connect.commit()

    def create_main_db(self):
        query_create = self.main_creating_query
        self.create_table(query_create)

    def run_query(self, query, new_data=None):
        with self.connect:
            if new_data:
                self.connect.execute(query, new_data)
                self.connect.commit()
            else:
                self.connect.execute(query)
                self.connect.commit()

    def delete(self, n):
        q = 'DELETE FROM weather WHERE n_id < (?);'
        self.run_query(q, (n,))

    def select(self, query):
        with self.connect:
            selected = self.connect.execute(query)
            return selected

    def drop(self):
        table_name = self.d_name
        query = f'DROP table {table_name}'
        self.query(query)

    def get_count(self):
        q = 'SELECT COUNT(*) FROM weather'
        return self.select(q)
