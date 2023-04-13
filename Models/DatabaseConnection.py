import sqlite3


class DatabaseConnection:
	
	@staticmethod
	def execute(self, query):
		conn = sqlite3.connect('diario.db')
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		conn.close()

