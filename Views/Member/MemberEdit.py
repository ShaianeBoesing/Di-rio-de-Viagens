from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.MemberController import MemberController


class MemberEdit(Screen):
	def __init__(self, member_id=None, **kwargs):
		super().__init__(**kwargs)
		self.member_id = member_id
		self.controller = MemberController()
		
		layout = GridLayout(cols=2)
		
		# Labels e Inputs
		name_label = Label(text='Nome:')
		layout.add_widget(name_label)
		self.name_input = TextInput(multiline=False)
		layout.add_widget(self.name_input)
		
		# Botões
		save_button = Button(text='Salvar')
		save_button.bind(on_press=self.save_member)
		layout.add_widget(save_button)
		
		cancel_button = Button(text='Cancelar')
		cancel_button.bind(on_press=self.cancel)
		layout.add_widget(cancel_button)
		
		# Adiciona o layout principal à tela
		self.add_widget(layout)
	
	def on_pre_enter(self, *args):
		if self.member_id is not None:
			member = self.controller.get_member(self.member_id)
			self.name_input.text = member['name']
	
	def save_member(self, *args):
		if not self.name_input.text.strip():
			popup = Popup(title='Erro', content=Label(text='O nome não pode ser deixado em branco.'), size_hint=(None, None), size=(400, 200))
			popup.open()
		else:
			self.controller.update_member(
				self.member_id,
				name=self.name_input.text
			)
			self.manager.current = 'member_list'
			self.manager.transition = SlideTransition(direction="right")
	
	def cancel(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="right")
