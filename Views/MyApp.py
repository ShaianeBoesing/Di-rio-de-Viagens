from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from Views.Member.MemberCreate import MemberCreate
from Views.Member.MemberList import MemberList
from Views.Main.MainView import MainView
from Views.Register.RegisterView import RegisterView
from Controllers.MemberController import MemberController
from Controllers.UserController import UserController
from kivymd.app import MDApp

class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(MyApp, self).__init__(**kwargs)
		self.__user_controller = UserController()
class MyApp(App):
	def __init__(self, **kwargs):
		super(MyApp, self).__init__(**kwargs)
		self.__user_controller = UserController()


		# Perform any necessary setup tasks here
	def build(self):
		sm = ScreenManager()
		sm.add_widget(MainView(name='main_view'))
		sm.add_widget(RegisterView(self.__user_controller, name='register_view'))
		sm.add_widget(MemberCreate(name='member_create'))
		sm.add_widget(MemberList(name='member_list'))
		return sm