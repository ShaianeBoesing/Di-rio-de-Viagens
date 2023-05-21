from Database.Database import Database


class Member:
	def __init__(self, name: str):
		self.__id = None
		self.__name = name
	
	def save(self):
		db = Database()
		if self.__id is None:
			values = {"name": self.__name}
			self.__id = db.insert("members", values)
		return self
	
	@staticmethod
	def show(member_id: int) -> 'Member':
		db = Database()
		result = db.select_by_id("members", member_id)
		if result is None:
			return None

		member = Member(result[1])
		member.__id = result[0]
		return member
	
	def update(self, **kwargs) -> None:
		db = Database()
		values = {"name": kwargs['name']}
		db.update("members", self.__id, values)
	
	def delete(self) -> None:
		db = Database()
		db.delete("members", self.__id)
		
	@staticmethod
	def list_by_traveller(traveller_id):
		db = Database()
		results = db.select(f"SELECT members.* FROM traveller_members JOIN members ON traveller_members.member_id = members.id WHERE traveller_members.traveller_id={traveller_id}")
		members = []
		for result in results:
			member = Member(result[1])
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
	def id(self):
		return self.__id
