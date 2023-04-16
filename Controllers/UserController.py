import sqlite3
from Models.User import User
from Models.Migrations.DatabaseConnection import DatabaseConnection as Db

class UserController:
    def __init__(self):
        self.conn = sqlite3.connect('../Models/Migrations/diario.db')
        self.create_user_table()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS viajantes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        senha TEXT NOT NULL
                                            )''')
        self.conn.commit()

    def register_user(self, username, name, password):
        # Check if the username is already taken
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM viajantes WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is not None:
            return False

        # Create a new user and add it to the database
        cursor.execute('INSERT INTO viajantes (username, nome, senha) VALUES (?, ?, ?)',
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