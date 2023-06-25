import datetime
from Database.Database import Database


class Comment:
	def __init__(self, description: str, spot_id: int):
		self.__spot_id = spot_id
		self.__description = description
		self.__id = None
		self.__date = None

	def save(self):
		db = Database()
		if self.__id is None:
			values = {
				"description": self.__description,
				"spot_id": self.__spot_id,
				"date": datetime.datetime.now()
			}
			self.__id = db.insert("comments", values)
		return self
	
	@staticmethod
	def show(comment_id: int) -> 'Comment':
		db = Database()
		result = db.select_by_id("comments", comment_id)
		if result is None:
			return None
		comment = Comment(result[1], result[3])
		comment.__id = result[0]
		return comment
	
	def update(self, **kwargs) -> None:
		db = Database()
		print(self.__dict__)
		values = {
			"description": kwargs['description']
		}
		db.update("comments", self.__id, values)
	
	def delete(self) -> None:
		db = Database()
		db.delete("comments", self.__id)
	
	@staticmethod
	def list_by_spot(spot_id):
		db = Database()
		results = db.select(
			f"SELECT id, description, date FROM comments WHERE comments.spot_id={spot_id}")
		comments = []
		for result in results:
			comment = Comment(result[1], spot_id)
			comment.__id = result[0]
			comment.__date = result[2]
			comments.append(comment)
		
		return comments
	
	@property
	def description(self) -> str:
		return self.__description
	
	@description.setter
	def description(self, description: str) -> None:
		self.__description = description
	
	@property
	def date(self) -> str:
		return self.__date
	
	@date.setter
	def date(self, date: str) -> None:
		self.__date = date
	
	@property
	def spot_id(self) -> str:
		return self.__spot_id
	
	@spot_id.setter
	def spot_id(self, spot_id) -> None:
		self.__spot_id = spot_id
	
	@property
	def id(self):
		return self.__id