from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.CommentController import CommentController


class CommentCreate(Screen):
	def __init__(self, controller: CommentController, my_app_instance, **kwargs):
		super().__init__(**kwargs)
		self.TEMP_SPOT_ID = 1
		self.my_app_instance = my_app_instance
		self.controller = controller
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
		
		layout.add_widget(Label(text="Criar Comentário"))
		
		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)
		
		input_grid.add_widget(Label(text="Descrição do Comentário:"))
		self.description_input = TextInput()
		input_grid.add_widget(self.description_input)
		
		button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
		layout.add_widget(button_grid)
		
		return_button = Button(text="Voltar")
		return_button.bind(on_press=self.on_return)
		button_grid.add_widget(return_button)
		register_button = Button(text="Salvar")
		register_button.bind(on_press=self.save_comment)
		button_grid.add_widget(register_button)
		
		self.add_widget(layout)
	
	def on_pre_enter(self, *args):
		self.description_input.text = ""
	
	def save_comment(self, *args):
		if not self.description_input.text.strip():
			popup = Popup(title='Erro', content=Label(text='A descrição não pode ser deixado em branco.'), size_hint=(None, None),
			              size=(400, 200))
			popup.open()
		else:
			spot_id = self.controller.trip_controller.current_spot.spot_database_id
			self.controller.create_comment(self.description_input.text.strip(), spot_id)
			self.manager.current = 'comment_list'
	
	def on_return(self, *args):
		self.manager.current = 'comment_list'
		self.manager.transition = SlideTransition(direction="left")

