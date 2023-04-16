import DatabaseConnection as db


class Membro:
  def __init__(self, name):
    self.__name = name
  
  def save(self):
    db.execute(f"""
      INSERT INTO membros(nome)
      VALUES ('{self.__name}')
    """)
  
  @classmethod
  def all(cls):
    db.execute(f""" SELECT * FROM membros """)
