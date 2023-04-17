from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from Controllers.MemberController import MemberController

class MemberList(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.members = []
		
	def on_pre_enter(self, *args):
		self.load()

	def load_members(self):
		self.members = MemberController.list_members_by_trip(1)
	def load(self):
		# Layout principal
		self.load_members()
		
		layout = BoxLayout(orientation='vertical')
		
		# Cabeçalho
		header_layout = BoxLayout(size_hint=(1, 0.1))
		header_label = Label(text="Lista de Membros", font_size='20sp', halign='center', valign='middle')
		header_layout.add_widget(header_label)
		layout.add_widget(header_layout)
		
		# Tabela
		scrollview = ScrollView()
		table_layout = GridLayout(cols=2, size_hint_y=None)
		table_layout.bind(minimum_height=table_layout.setter('height'))
		
		for member in self.members:
			name_label = Label(text=member['name'], font_size='16sp', halign='center', valign='middle')
			actions_layout = BoxLayout(size_hint_y=None, padding=10, size_hint=(None, None), size=(400, dp(40)), minimum_height=dp(40))
			actions_layout.cols = 2  # definir duas colunas
			actions_layout.col_default_width = 200  # definir largura da coluna como 200 pixels
			edit_button = Button(text="Editar", size_hint=(None, None), size=(200, dp(40)), font_size='16sp')
			delete_button = Button(text="Excluir", size_hint=(None, None), size=(200, dp(40)), font_size='16sp')
			actions_layout.add_widget(edit_button)
			actions_layout.add_widget(delete_button)
			table_layout.add_widget(name_label)
			table_layout.add_widget(actions_layout)
		scrollview.add_widget(table_layout)
		layout.add_widget(scrollview)
		
		# Botões
		buttons_layout = BoxLayout(size_hint=(1, 0.1), padding=10)
		back_button = Button(text="Voltar", font_size='18sp')
		new_button = Button(text="Novo", font_size='18sp')
		buttons_layout.add_widget(back_button)
		buttons_layout.add_widget(new_button)
		layout.add_widget(buttons_layout)
		
		# Adiciona o layout principal à tela
		self.add_widget(layout)
		
		# Adiciona os callbacks aos botões
		back_button.bind(on_release=self.on_back)
		new_button.bind(on_release=self.on_new_member)
	
	def on_new_member(self, *args):
		self.manager.current = 'member_create'
		self.manager.transition = SlideTransition(direction="right")
	
	def on_back(self, *args):
		self.manager.current = 'member_list'
		self.manager.transition = SlideTransition(direction="left")


