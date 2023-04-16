import sqlite3

conn = sqlite3.connect('diario.db')

cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE viajantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
  );
""")

cursor.execute("""
CREATE TABLE viagens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  status TEXT NOT NULL,
  viajante_id INTEGER NOT NULL,
  FOREIGN KEY(viajante_id) REFERENCES viajantes(id)
);
""")

cursor.execute("""
  CREATE TABLE membros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    qtd_spot_visitados INTEGER NOT NULL,
    qtd_viagens_visitados INTEGER NOT NULL,
    viajante_id INTEGER NOT NULL,
    FOREIGN KEY(viajante_id) REFERENCES viajantes(id)
  );
""")

cursor.execute("""
  CREATE TABLE spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    hora_inicio DATETIME NOT NULL,
    hora_fim DATETIME NOT NULL,
    status TEXT NOT NULL,
    valor REAL NOT NULL,
    viagem_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY(viagem_id) REFERENCES viagens(id),
    FOREIGN KEY(categoria_id) REFERENCES categorias(id)
  );
""")

cursor.execute("""
  CREATE TABLE comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comentario TEXT NOT NULL,
    data DATETIME NOT NULL,
    spot_id INTEGER NOT NULL,
    FOREIGN KEY(spot_id) REFERENCES spots(id)
  );
""")

cursor.execute("""
CREATE TABLE categorias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  valor_medio_gasto REAL NOT NULL,
  viajante_id INTEGER NOT NULL,
  FOREIGN KEY(viajante_id) REFERENCES viajantes(id)
);
""")

cursor.execute("""
  CREATE TABLE spot_membro (
    spot_id INTEGER NOT NULL,
    membro_id INTEGER NOT NULL,
    PRIMARY KEY(spot_id, membro_id),
    FOREIGN KEY(spot_id) REFERENCES spots(id),
    FOREIGN KEY(membro_id) REFERENCES membros(id)
  );
""")

print('Schemas criados com sucesso.')

conn.close()
