from kivy.app import App
from Views.Main.MainView import MainView

class MyApp(App):
    def build(self):
        return MainView()
