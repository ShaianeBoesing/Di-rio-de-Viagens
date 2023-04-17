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
		# self.controller = MemberController()
		# self.layout = GridLayout(cols=2)
		# self.add_widget(self.layout)
		# self.name_label = Label(text='Nome:')
		# self.layout.add_widget(self.name_label)
		# self.name_input = TextInput(multiline=False)
		# self.layout.add_widget(self.name_input)
		# self.save_button = Button(text='Salvar')
		# self.save_button.bind(on_press=self.save_member)
		# self.layout.add_widget(self.save_button)
		# self.cancel_button = Button(text='Voltar')
		# self.cancel_button.bind(on_press=self.cancel)
		# self.layout.add_widget(self.cancel_button)
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

		# Add the "Registrar" label to the layout
		layout.add_widget(Label(text="Criar membro"))

		# Create a GridLayout to hold the input fields
		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)

		# Add the "Nome de Usuário" label and text input to the input grid
		input_grid.add_widget(Label(text="Nome do membro:"))
		self.name_input = TextInput()
		input_grid.add_widget(self.name_input)

		# Create a GridLayout to hold the buttons
		button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
		layout.add_widget(button_grid)

		# Create the "Voltar" button and bind it to the on_return function
		return_button = Button(text="Voltar")
		return_button.bind(on_press=self.on_return)
		button_grid.add_widget(return_button)

		# Create the "Registrar" button and bind it to the on_register function
		register_button = Button(text="Criar Membro")
		register_button.bind(on_press=self.save_member)
		button_grid.add_widget(register_button)

		# Add the register layout to the screen
		self.add_widget(layout)
	
	def on_pre_enter(self, *args):
		self.name_input.text = ""
	
	def save_member(self, *args):
		if not self.name_input.text.strip():
			popup = Popup(title='Erro', content=Label(text='O nome não pode ser deixado em branco.'), size_hint=(None, None), size=(400, 200))
			popup.open()
		else:
			MemberController.create_member(self.name_input.text)
			self.manager.current = 'member_list'
	
	def on_return(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="left")

