from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Controllers.MemberController import MemberController


class MemberEdit(Screen):
	def __init__(self, controller: MemberController, my_app_instance, member_id=None, **kwargs):
		super().__init__(**kwargs)
		self.member_id = member_id
		self.controller = controller
		self.my_app_instance = my_app_instance
		layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
		
		layout.add_widget(Label(text="Editar Membro"))

		input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
		layout.add_widget(input_grid)

		input_grid.add_widget(Label(text="Nome do membro:"))
		self.name_input = TextInput(multiline=False)
		input_grid.add_widget(self.name_input)
		
		button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
		layout.add_widget(button_grid)

		return_button = Button(text="Voltar")
		return_button.bind(on_press=self.on_return)
		button_grid.add_widget(return_button)
		register_button = Button(text="Salvar")
		register_button.bind(on_press=self.save_member)
		button_grid.add_widget(register_button)

		self.add_widget(layout)
	
	def on_pre_enter(self, *args):
		if self.member_id is not None:
			member = self.controller.get_member(self.member_id)
			self.name_input.text = member['name']
	
	def save_member(self, *args):
		is_valid_member = self.validate_member()
		if is_valid_member:
			self.controller.update_member(
				member_id=self.member_id,
				name=self.name_input.text
			)
			self.manager.current = 'member_list'
			self.manager.transition = SlideTransition(direction="right")
	
	def on_return(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="right")
	
	def validate_member(self):
		return self.validate_has_content() and self.validate_is_unique()
	
	def validate_has_content(self):
		has_content = self.name_input.text.strip()
		if not has_content:
			popup = Popup(title='Erro', content=Label(text='O nome não pode ser deixado em branco.'), size_hint=(None, None),
			              size=(400, 200))
			popup.open()
		
		return has_content
	
	def validate_is_unique(self):
		is_unique = self.controller.name_is_valid(self.name_input.text.strip(), self.my_app_instance.traveller_id, self.member_id)
		print(is_unique)
		if not is_unique:
			popup = Popup(title='Erro', content=Label(text='Este nome já existe.'), size_hint=(None, None), size=(400, 200))
			popup.open()
		return is_unique
