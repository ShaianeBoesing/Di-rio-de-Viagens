from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.MemberController import MemberController


class MemberCreate(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.controller = MemberController()
		self.layout = GridLayout(cols=2)
		self.add_widget(self.layout)
		self.name_label = Label(text='Nome:')
		self.layout.add_widget(self.name_label)
		self.name_input = TextInput(multiline=False)
		self.layout.add_widget(self.name_input)
		self.save_button = Button(text='Salvar')
		self.save_button.bind(on_press=self.save_member)
		self.layout.add_widget(self.save_button)
		self.cancel_button = Button(text='Voltar')
		self.cancel_button.bind(on_press=self.cancel)
		self.layout.add_widget(self.cancel_button)
	
	def on_pre_enter(self, *args):
		self.name_input.text = ""
	
	def save_member(self, *args):
		if not self.name_input.text.strip():
			popup = Popup(title='Erro', content=Label(text='O nome não pode ser deixado em branco.'), size_hint=(None, None), size=(400, 200))
			popup.open()
		else:
			self.controller.create_member(self.name_input.text)
			self.manager.current = 'member_list'
	
	def cancel(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="left")

