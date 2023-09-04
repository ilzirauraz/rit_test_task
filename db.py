import sqlite3


class SQLiteDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(e)

    def execute(self, query, params=None):
        if self.conn is None:
            self.connect()
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def close(self):
        if self.conn:
            self.conn.close()
