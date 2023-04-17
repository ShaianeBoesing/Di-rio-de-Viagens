from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Views.Member.MemberCreate import MemberCreate
from Views.Member.MemberList import MemberList
from Views.Member.MemberEdit import MemberEdit


class WindowManager(ScreenManager):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class MyApp(App):
	def build(self):
		self.manager = WindowManager()
		self.manager.add_widget(MemberList(name='member_list'))
		self.manager.add_widget(MemberCreate(name='member_create'))
		self.manager.add_widget(MemberEdit(name='member_edit'))
		return self.manager
