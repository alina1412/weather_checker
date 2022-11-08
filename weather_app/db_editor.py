"""
class for connecting to sqlite db
"""

import sqlite3


class DatabaseEditor:
    """make connection to sqlite3 db, creates table, runs query"""

    def __init__(self) -> None:
        self.database_name = "last_weather.db"
        self.table_name = "weather"
        self.connect = None
        self.make_connection()
        self.main_creating_query = f"""
            CREATE TABLE IF not EXISTS
             {self.table_name} (
                n_id INTEGER PRIMARY KEY,
                city varchar(255),
                weather int
            )
        """
        self.create_main_db()

    def close(self) -> None:
        if self.connect:
            self.connect.close()

    def make_connection(self) -> None:
        try:
            connect = sqlite3.connect(self.database_name)
            self.connect = connect
        except sqlite3.Error as error:
            print(error)

    def create_table(self, query) -> None:
        with self.connect:
            cursor = self.connect.cursor()
            cursor.execute(query)
            self.connect.commit()

    def create_main_db(self) -> None:
        query_create = self.main_creating_query
        self.create_table(query_create)

    def run_query(self, query, new_data=None) -> None:
        with self.connect:
            if new_data:
                self.connect.execute(query, new_data)
                self.connect.commit()
            else:
                self.connect.execute(query)
                self.connect.commit()

    def delete(self, n_id) -> None:
        query = f"DELETE FROM {self.table_name} WHERE n_id < (?);"
        self.run_query(query, (n_id,))

    def select(self, query) -> list:
        with self.connect:
            selected = self.connect.execute(query)
            return list(selected)

    def drop(self) -> None:
        query = f"DROP table {self.table_name}"
        self.run_query(query)

    def get_count(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        return self.select(query)[0][0]
