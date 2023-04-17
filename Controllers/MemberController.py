from typing import List
from Model.Member import Member

class MemberController:
	@staticmethod
	def create_member(name: str) -> Member:
		trip_id = 1
		member = Member(name, trip_id)
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
	def list_members_by_trip(trip_id=None):
		# Se o ID da viagem não for fornecido, retorna uma lista vazia
		if trip_id is None:
			return []
		
		results = Member.list_by_trip(trip_id)
		# results = db.select(
		
		# Cria uma lista de objetos Member com as informações da consulta
		members = []
		for result in results:
			member = {'name': result.name, 'id': result.id}
			members.append(member)
		
		return members
	