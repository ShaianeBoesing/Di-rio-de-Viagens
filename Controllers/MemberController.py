from typing import List
from Model.Member import Member
from Model.TravellerMembers import TravellerMembers

class MemberController:
	def __init__(self):
		self.__table_name = 'members'

	@staticmethod
	def create_member(name: str, traveller_id) -> Member:
		new_member = Member(name)
		member = new_member.save()
		new_traveller_member = TravellerMembers(member.id, traveller_id)
		new_traveller_member.save()
		return member
	
	@staticmethod
	def get_member(member_id: int) -> Member:
		member = Member.show(member_id)
		return {
			'id': member.id,
			'name': member.name,
		}
	def update_member(self, member_id: int, **kwargs) -> None:
		member = Member.show(member_id)
		if member:
			member.update(**kwargs)
	
	@staticmethod
	def delete_member(member_id: int) -> None:
		member = Member.show(member_id)
		if member:
			member.delete()
	
	@staticmethod
	def list_members_by_traveller(traveller_id=None):
		if traveller_id is None:
			return []
		
		results = Member.list_by_traveller(traveller_id)
		members = []
		for result in results:
			member = {'name': result.name, 'id': result.id}
			members.append(member)
		
		return members
	