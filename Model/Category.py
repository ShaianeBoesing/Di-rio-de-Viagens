from Database.Database import Database


class Category:
	def __init__(self, name: str):
		self.__id = None
		self.__name = name
	
	def save(self):
		db = Database()
		if self.__id is None:
			values = {"name": self.__name}
			self.__id = db.insert("categories", values)
		return self
	
	@staticmethod
	def show(category_id: int) -> 'Category':
		db = Database()
		result = db.select_by_id("categories", category_id)
		if result is None:
			return None
		
		category = Category(result[1])
		category.__id = result[0]
		return category
	
	def update(self, **kwargs) -> None:
		db = Database()
		values = {"name": kwargs['name']}
		db.update("categories", self.__id, values)
	
	def delete(self) -> None:
		db = Database()
		db.delete("categories", self.__id)
	
	@staticmethod
	def list_by_traveller(traveller_id):
		db = Database()
		results = db.select(
			f"SELECT categories.* FROM traveller_categories JOIN categories ON traveller_categories.category_id = categories.id WHERE traveller_categories.traveller_id={traveller_id}")
		categories = []
		for result in results:
			category = Category(result[1])
			category.__id = result[0]
			categories.append(category)
		
		return categories
	
	@property
	def name(self) -> str:
		return self.__name
	
	@name.setter
	def name(self, name: str) -> None:
		self.__name = name
	
	@property
	def id(self):
		return self.__id
