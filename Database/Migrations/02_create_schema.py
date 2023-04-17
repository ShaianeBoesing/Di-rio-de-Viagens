import sqlite3

conn = sqlite3.connect('diary.db')

cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE travellers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
  );
""")

cursor.execute("""
  CREATE TABLE trips (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  title TEXT NOT NULL,
	  start_date DATE NOT NULL,
	  end_date DATE NOT NULL,
	  status TEXT NOT NULL,
	  traveller_id INTEGER NOT NULL,
	  FOREIGN KEY(traveller_id) REFERENCES travellers(id)
	);
""")

cursor.execute("""
  CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    trip_id INTEGER NOT NULL,
    FOREIGN KEY(trip_id) REFERENCES trips(id)
  );
""")

cursor.execute("""
  CREATE TABLE spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_hour DATETIME NOT NULL,
    end_hour DATETIME NOT NULL,
    status TEXT NOT NULL,
    value REAL NOT NULL,
    trip_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY(trip_id) REFERENCES trips(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
  );
""")

cursor.execute("""
  CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    spot_id INTEGER NOT NULL,
    FOREIGN KEY(spot_id) REFERENCES spots(id)
  );
""")

cursor.execute("""
	CREATE TABLE categories (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  name TEXT NOT NULL,
	  average_spent REAL NOT NULL,
	  traveller_id INTEGER NOT NULL,
	  FOREIGN KEY(traveller_id) REFERENCES traveller(id)
	);
""")

cursor.execute("""
  CREATE TABLE spot_members (
    spot_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    PRIMARY KEY(spot_id, member_id),
    FOREIGN KEY(spot_id) REFERENCES spots(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
  );
""")

print('Schemas criados com sucesso.')

conn.close()
