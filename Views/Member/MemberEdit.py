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
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
		
		# Adiciona título ao layout
		layout.add_widget(Label(text="Editar Membro"))

		# cria GridLayout para os inputs e adiciona ao Layout Base
		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)

		#Adiciona Label e Input ao input_grid de inputs
		input_grid.add_widget(Label(text="Nome do membro:"))
		self.name_input = TextInput(multiline=False)
		input_grid.add_widget(self.name_input)
		
		# cria GridLayout para os buttons e adiciona ao Layout Base
		button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
		layout.add_widget(button_grid)


		# cria botões de voltar e salvar e adiciona ao button_grid
		return_button = Button(text="Voltar")
		return_button.bind(on_press=self.on_return)
		button_grid.add_widget(return_button)
		register_button = Button(text="Salvar")
		register_button.bind(on_press=self.save_member)
		button_grid.add_widget(register_button)

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
				member_id=self.member_id,
				name=self.name_input.text
			)
			self.manager.current = 'member_list'
			self.manager.transition = SlideTransition(direction="right")
	
	def on_return(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="right")
