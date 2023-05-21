from Database.Database import Database


class TravellerCategories:
	def __init__(self, category_id, traveller_id):
		self.__category_id = category_id
		self.__traveller_id = traveller_id
	
	def save(self):
		db = Database()
		values = {
			'category_id': self.__category_id,
			'traveller_id': self.__traveller_id
		}
		db.insert('traveller_categories', values)
	
	def delete(self):
		db = Database()
		db.delete('traveller_categories', self.__category_id)
	
	@staticmethod
	def show(traveller_id):
		db = Database()
		return db.select_by_id('traveller_categories', traveller_id)
	
	@property
	def category_id(self):
		return self.__category_id
	
	@category_id.setter
	def category_id(self, category_id):
		self.__category_id = category_id
	
	@property
	def traveller_id(self):
		return self.__traveller_id
	
	@traveller_id.setter
	def traveller_id(self, traveller_id):
		self.__traveller_id = traveller_id

