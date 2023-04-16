import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('diary.db')
        self.cursor = self.connection.cursor()

    def insert(self, table_name, values):
        columns = ','.join(values.keys())
        params = ','.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        self.cursor.execute(query, tuple(values.values()))
        self.connection.commit()

    def select_all(self, table_name):
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_by_id(self, table_name, id):
        query = f"SELECT * FROM {table_name} WHERE id=?"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def update(self, table_name, id, values):
        set_values = ', '.join([f"{column} = ?" for column in values.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE id=?"
        params = list(values.values())
        params.append(id)
        self.cursor.execute(query, params)
        self.connection.commit()

    def delete(self, table_name, id):
        query = f"DELETE FROM {table_name} WHERE id=?"
        self.cursor.execute(query, (id,))
        self.connection.commit()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_last_id(self):
        query = "SELECT last_insert_rowid()"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def __del__(self):
        self.connection.close()
