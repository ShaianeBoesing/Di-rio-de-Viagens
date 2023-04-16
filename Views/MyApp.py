from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from Views.Main.MainView import MainView
from Views.Register.RegisterView import RegisterView

from kivymd.app import MDApp

class WindowManager(ScreenManager):
	pass

Builder.load_file("Views/TravelDiary.kv")

class MyApp(App):
	def build(self):
		self.title = 'Diário de Viagens'
		return WindowManager()
  