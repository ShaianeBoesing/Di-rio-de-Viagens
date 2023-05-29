from typing import List
from Model.Member import Member

class MemberController:
	def __init__(self):
		self.__table_name = 'members'

	def create_member(self, name: str, traveller_id) -> Member:
		new_member = Member(name)
		member = new_member.save()
		new_member.save_traveller_member(traveller_id)
		return member
	
	def get_member(self, member_id: int) -> Member:
		member = Member.show(member_id)
		return {
			'id': member.id,
			'name': member.name,
		}
	def update_member(self, member_id: int, **kwargs) -> None:
		member = Member.show(member_id)
		if member:
			member.update(**kwargs)
	
	def delete_member(self, member_id: int) -> None:
		member = Member.show(member_id)
		if member:
			member.delete()
	
	def list_members_by_traveller(self, traveller_id=None):
		if traveller_id is None:
			return []
		
		results = Member.list_by_traveller(traveller_id)
		members = []
		for result in results:
			member = {'name': result.name, 'id': result.id}
			members.append(member)
		
		return members
	
	def name_is_valid(self, name: str, traveller_id: int) -> bool:
		return Member.validate_member_name_by_traveller(name, traveller_id)
