from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from Controllers import MemberController


class MemberList(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.add_widget(self.layout)
        self.members = []

    def add_member(self, member_data):
        self.members.append(member_data)

    def clear_members(self):
        self.members = []
        self.layout.clear_widgets()

