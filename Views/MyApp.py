from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Views.Member.MemberCreate import MemberCreate
from Views.Member.MemberList import MemberList

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MyApp(App):
	def build(self):
		sm = WindowManager()
		sm.add_widget(MemberList(name='member_list'))
		sm.add_widget(MemberCreate(name='member_create'))
		return sm