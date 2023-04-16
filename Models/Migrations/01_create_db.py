import sqlite3

conn = sqlite3.connect('diario.db')

print('Banco criada com sucesso.')

conn.close()
