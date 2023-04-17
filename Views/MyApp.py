from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from Views.Member.MemberCreate import MemberCreate
from Views.Member.MemberList import MemberList
from Controllers.MemberController import MemberController
from kivymd.app import MDApp

class WindowManager(ScreenManager):
	pass

class MyApp(App):
	def build(self):
		sm = ScreenManager()
		sm.add_widget(MemberCreate(name='member_create'))
		sm.add_widget(MemberList(name='member_list'))
		return sm