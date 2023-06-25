from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.CommentController import CommentController


class CommentEdit(Screen):
	def __init__(self, controller: CommentController, my_app_instance, comment_id=None, **kwargs):
		super().__init__(**kwargs)
		self.comment_id = comment_id
		self.controller = controller
		self.TEMP_TRAVELLER_ID = 1
		self.my_app_instance = my_app_instance
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
		
		layout.add_widget(Label(text="Editar Categoria"))
		
		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)
		
		input_grid.add_widget(Label(text="Descrição do Categoria:"))
		self.descricao_input = TextInput(multiline=True)
		input_grid.add_widget(self.descricao_input)
		
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
		if self.comment_id is not None:
			comment = self.controller.get_comment(self.comment_id)
			self.descricao_input.text = comment['description']
	
	def save_comment(self, *args):
		if not self.descricao_input.text.strip():
			popup = Popup(title='Erro', content=Label(text='O descricao não pode ser deixado em branco.'), size_hint=(None, None),
			              size=(400, 200))
			popup.open()
		else:
			print(self.comment_id, self.descricao_input.text)
			self.controller.update_comment(
				comment_id=self.comment_id,
				description=self.descricao_input.text.strip()
			)
			self.manager.current = 'comment_list'
			self.manager.transition = SlideTransition(direction="right")
	
	def on_return(self, *args):
		self.manager.current = 'comment_list'
		self.manager.transition = SlideTransition(direction="right")
