from Database.Database import Database


class Member:
	def __init__(self, name: str, trip_id: int):
		self.__trip_id = trip_id
		self.__name = name
		self.__id = None
	
	def save(self) -> None:
		# Conexão com o banco de dados
		db = Database()
		
		# Verifica se o objeto já existe no banco de dados (a partir do id)
		if self.__id is None:
			# Insere um novo objeto no banco de dados
			values = {"name": self.__name, "trip_id": self.__trip_id}
			self.__id = db.insert("members", values)
		else:
			# Atualiza um objeto existente no banco de dados
			values = {"name": self.__name}
			db.update("members", name=self.__name)
	
	@staticmethod
	def show(member_id: int) -> 'Member':
		# Conexão com o banco de dados
		db = Database()
		
		# Faz a consulta no banco de dados
		result = db.select_by_id("members", member_id)
		
		# Se o resultado da consulta for nulo, retorna None
		if result is None:
			return None
		
		# Cria e retorna um objeto Member com as informações da consulta
		member = Member(result[1], result[2])
		member.__id = result[0]
		return member
	
	def update(self, **kwargs) -> None:
		# Atualiza os atributos do objeto com os novos valores
		db = Database()

		# Salva as informações atualizadas no banco de dados
		values = {"name": kwargs['name']}
		db.update("members", self.__id, values)
	
	def delete(self) -> None:
		# Conexão com o banco de dados
		db = Database()
		
		# Deleta o objeto do banco de dados
		db.delete("members", self.__id)
	
	def spots_counter(self) -> int:
		# Conexão com o banco de dados
		db = Database()
		
		# Faz a consulta no banco de dados
		result = db.select(f"SELECT COUNT(*) FROM spots WHERE member_id={self.__id}")
		
		# Retorna o resultado da consulta
		return result[0][0]
	
	def travels_counter(self) -> int:
		# Conexão com o banco de dados
		db = Database()
		
		# Faz a consulta no banco de dados
		result = db.select(f"SELECT COUNT(*) FROM trips WHERE member_id={self.__id}")
		
		# Retorna o resultado da consulta
		return result[0][0]
	
	@staticmethod
	def list_by_trip(trip_id: int):
		# Conexão com o banco de dados
		db = Database()
		
		# Faz a consulta no banco de dados para obter a lista de membros
		results = db.select(f"SELECT * FROM members WHERE trip_id={trip_id}")

		# Cria uma lista de objetos Member com as informações da consulta
		members = []
		for result in results:
			member = Member(result[1], result[2])
			member.__id = result[0]
			members.append(member)
		
		return members
	
	@property
	def name(self) -> str:
		return self.__name
	
	@name.setter
	def name(self, name: str) -> None:
		self.__name = name
	
	@property
	def trip_id(self) -> str:
		return self.__trip_id
	
	@trip_id.setter
	def trip_id(self, trip_id: int) -> None:
		self.__trip_id = trip_id
	
	@property
	def id(self):
		return self.__id
