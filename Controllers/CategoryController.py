from typing import List
from Model.Category import Category


class CategoryController:
	def __init__(self):
		self.__table_name = 'categories'
	
	def create_category(self, name: str, traveller_id) -> Category:
		new_category = Category(name)
		category = new_category.save()
		new_category.save_traveller_category(traveller_id)
		return category
	
	def get_category(self, category_id: int) -> Category:
		category = Category.show(category_id)
		return {
			'id': category.id,
			'name': category.name,
		}
	
	def update_category(self, category_id: int, **kwargs) -> None:
		category = Category.show(category_id)
		if category:
			category.update(**kwargs)
	
	def delete_category(self, category_id: int) -> None:
		category = Category.show(category_id)
		if category:
			category.delete()
	
	def list_categories_by_traveller(self, traveller_id=None):
		if traveller_id is None:
			return []
		
		results = Category.list_by_traveller(traveller_id)
		categories = []
		for result in results:
			category = {'name': result.name, 'id': result.id}
			categories.append(category)
		
		return categories
	
	def name_is_valid(self, name: str, traveller_id: int, category_id=None) -> bool:
		return Category.validate_category_name_by_traveller(name, traveller_id, category_id)
