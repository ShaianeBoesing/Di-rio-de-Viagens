from typing import List
from Model.Member import Member

class MemberController:
	@staticmethod
	def create_member(name: str) -> Member:
		member = Member(name)
		member.save()
		return member
	
	@staticmethod
	def get_member(member_id: int) -> Member:
		return Member.show(member_id)
	
	@staticmethod
	def update_member(member_id: int, **kwargs) -> None:
		member = Member.show(member_id)
		if member:
			member.update(**kwargs)
	
	@staticmethod
	def delete_member(member_id: int) -> None:
		member = Member.show(member_id)
		if member:
			member.delete()
	
	@staticmethod
	def list_members_by_trip():
		pass

	@staticmethod
	def list_members_by_trip():
		pass
