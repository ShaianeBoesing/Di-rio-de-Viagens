import sqlite3

conn = sqlite3.connect('diary.db')

print('Banco criado com sucesso.')

conn.close()
