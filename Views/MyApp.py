from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from Views.Main.MainView import MainView
from Views.Register.RegisterView import RegisterView

class WindowManager(ScreenManager):
	pass

kv = Builder.load_file("Views/my.kv")
class MyApp(App):
	def build(self):
		return kv
