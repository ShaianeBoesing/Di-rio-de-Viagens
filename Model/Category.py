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
		self.delete_traveller_category()
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
	
	# Relacionamento Category e Traveller
	def save_traveller_category(self, traveller_id):
		db = Database()
		values = {
			'category_id': self.__id,
			'traveller_id': traveller_id
		}
		db.insert('traveller_categories', values)
	
	def get_traveller_id_for_category(self):
		db = Database()
		category_id = self.__id
		query = f"SELECT traveller_id FROM traveller_categories WHERE category_id={category_id}"
		result = db.select(query)
		if result:
			return result[0][0]
		return None
	
	def delete_traveller_category(self):
		db = Database()
		category_id = self.__id
		traveller_id = self.get_traveller_id_for_category()
		query = f"DELETE FROM traveller_categories WHERE category_id={category_id} AND traveller_id={traveller_id}"
		db.raw_sql(query)

	@staticmethod
	def validate_category_name_by_traveller(name: str, traveller_id: int, category_id=None) -> bool:
		db = Database()
		query = f"SELECT * FROM categories JOIN traveller_categories ON categories.id = traveller_categories.category_id WHERE categories.name = '{name}' AND traveller_categories.traveller_id = {traveller_id}"
		if category_id is not None:
			query += f"AND categories.id <> {category_id}"
		result = db.select(query)
		return len(result) == 0
	