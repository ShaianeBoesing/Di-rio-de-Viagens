import sqlite3

conn = sqlite3.connect('diary.db')

cursor = conn.cursor()

# Inserir dados na tabela travellers
cursor.execute("""
  INSERT INTO travellers (name, username, password)
  VALUES ('Alice', 'alice123', 'password123');
""")

# Inserir dados na tabela trips
cursor.execute("""
  INSERT INTO trips (title, start_date, end_date, status, traveller_id)
  VALUES ('Viagem à Praia', '2023-06-01', '2023-06-10', 'Planejada', 1);
""")

# Inserir dados na tabela members
cursor.execute("""
  INSERT INTO members (name, traveller_id)
  VALUES ('Bob', 1);
""")

# Inserir dados na tabela spots
cursor.execute("""
  INSERT INTO spots (name, start_hour, end_hour, status, value, trip_id, category_id)
  VALUES ('Praia do Rosa', '2023-06-02 10:00:00', '2023-06-02 18:00:00', 'Concluído', 100.00, 1, 1);
""")

# Inserir dados na tabela comments
cursor.execute("""
  INSERT INTO comments (description, date, spot_id)
  VALUES ('Lugar incrível!', '2023-06-02 18:30:00', 1);
""")

# Inserir dados na tabela categories
cursor.execute("""
  INSERT INTO categories (name, average_spent, traveller_id)
  VALUES ('Comida', 50.00, 1);
""")

# Inserir dados na tabela spot_members
cursor.execute("""
  INSERT INTO spot_members (spot_id, member_id)
  VALUES (1, 1);
""")

# Salvar as alterações
conn.commit()

print('Dados inseridos com sucesso.')

conn.close()
