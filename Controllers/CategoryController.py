from typing import List
from Model.Category import Category


class CategoryController:
	def __init__(self, trip_controller_instance):
		self.__table_name = 'categories'
		#category controller precisa se comunicar com ele
		self.__trip_controller = trip_controller_instance
	
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

	def get_category_cost_for_trip(self, category_id, traveller_id):
		trips = self.trip_controller.get_all_trips_from_traveller(traveller_id)
		sum = 0
		spot_with_cat_counter = 0
		highest_value = 0
		for trip in trips:
			for spot in trip.spots:
				if spot.category.id == category_id:
					if spot.money_spent > highest_value:
						highest_value = spot.money_spent
					sum += (spot.money_spent)
					spot_with_cat_counter += 1

		if spot_with_cat_counter == 0:
			return 0, 0
		else:
			return sum, sum/spot_with_cat_counter, highest_value


	@property
	def trip_controller(self):
		return self.__trip_controller
