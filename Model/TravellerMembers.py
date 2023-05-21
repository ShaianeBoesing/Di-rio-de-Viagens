from Database.Database import Database


class TravellerMembers:
	def __init__(self, member_id, traveller_id):
		self.__member_id = member_id
		self.__traveller_id = traveller_id

	def save(self):
		db = Database()
		values = {
			'member_id': self.__member_id,
			'traveller_id': self.__traveller_id
		}
		db.insert('traveller_members', values)
		
	def delete(self):
		db = Database()
		db.delete('traveller_members', self.__member_id)
	
	@staticmethod
	def show(traveller_id):
		db = Database()
		return db.select_by_id('traveller_members', traveller_id)
	
	@property
	def member_id(self):
		return self.__member_id

	@member_id.setter
	def member_id(self, member_id):
		self.__member_id = member_id
	
	@property
	def traveller_id(self):
		return self.__traveller_id
	
	@traveller_id.setter
	def traveller_id(self, traveller_id):
		self.__traveller_id = traveller_id
	
