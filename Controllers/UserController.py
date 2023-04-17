import sqlite3
from Model.User import User
import _md5

class UserController:
    def __init__(self):
        self.conn = sqlite3.connect('../Database/Migrations/diary.db')
        self.create_user_table()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS travellers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL
                                            )''')
        self.conn.commit()

    def register_user(self, username, name, password):
        # Check if the username is already taken
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM travellers WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is not None:
            print("deu nao")
            return False

        # Create a new user and add it to the database
        cursor.execute('INSERT INTO travellers (username, name, password) VALUES (?, ?, ?)',
                       (username, name, password))
        self.conn.commit()
        return True

    def get_user_by_username(self, username):
        # Retrieve a user by username
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM viajantes WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is None:
            return None
        return User(result[1], result[2], result[3])

a = UserController()
a.register_user('asad','123','asdv')