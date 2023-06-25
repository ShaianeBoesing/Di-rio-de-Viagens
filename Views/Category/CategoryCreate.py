from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.CategoryController import CategoryController


class CategoryCreate(Screen):
	def __init__(self, controller: CategoryController, my_app_instance, **kwargs):
		super().__init__(**kwargs)
		self.my_app_instance = my_app_instance
		self.controller = controller
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

		layout.add_widget(Label(text="Criar Categoria"))

		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)
		
		input_grid.add_widget(Label(text="Nome do Categoria:"))
		self.name_input = TextInput()
		input_grid.add_widget(self.name_input)
		
		button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
		layout.add_widget(button_grid)

		return_button = Button(text="Voltar")
		return_button.bind(on_press=self.on_return)
		button_grid.add_widget(return_button)
		register_button = Button(text="Salvar")
		register_button.bind(on_press=self.save_category)
		button_grid.add_widget(register_button)

		self.add_widget(layout)
	
	def on_pre_enter(self, *args):
		self.name_input.text = ""
	
	def save_category(self, *args):
		is_valid_category = self.validate_category()
		if is_valid_category:
			self.controller.create_category(self.name_input.text, self.my_app_instance.traveller_id)
			self.manager.current = 'category_list'
	
	def on_return(self, *args):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'category_list'

