from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from Controllers.MemberController import MemberController

class MemberList(Screen):
	def __init__(self, controller: MemberController, **kwargs):
		super().__init__(**kwargs)
		self.members = []
		self.controller = controller
		self.TEMP_TRAVELLER_ID = 1

	def on_pre_enter(self, *args):
		self.load()
	
	def load_members(self):
		self.members = self.controller.list_members_by_traveller(self.TEMP_TRAVELLER_ID)
	
	def load(self):
		self.clear_widgets() # Limpa todos os widgets da tela para não se sobrepor
		self.load_members() # Carrega o self.members
		
		# Layout principal
		layout = BoxLayout(orientation='vertical')
		
		# Cabeçalho
		header_layout = BoxLayout(size_hint=(1, 0.1))
		header_label = Label(text="Lista de Membros", font_size='20sp', halign='center', valign='middle')
		header_layout.add_widget(header_label)
		layout.add_widget(header_layout)
		
		# Tabela
		scrollview = ScrollView()
		table_layout = GridLayout(cols=2, size_hint_y=None, padding=(30, 50, 30, 50))
		table_layout.bind(minimum_height=table_layout.setter('height'))
		
		for member in self.members:
			name_label = Label(text=member['name'], font_size='16sp', halign='center', valign='middle')
			
			# Layout para actions
			actions_layout = BoxLayout(size_hint_y=None, padding=10, size_hint=(None, None), size=(400, dp(40)), minimum_height=dp(40))
			actions_layout.cols = 2  # definir duas colunas
			actions_layout.col_default_width = 200  # definir largura da coluna como 200 pixels

			# Adiciona o nome à coluna 1 e actions_layout à coluna 2 do table_layout
			table_layout.add_widget(name_label)
			table_layout.add_widget(actions_layout)

			# Botão de actions
			edit_button = Button(text="Editar", size_hint=(None, None), size=(200, dp(40)), font_size="16sp")
			delete_button = Button(text="Excluir", size_hint=(None, None), size=(200, dp(40)), font_size="16sp")
			edit_button.bind(on_release=lambda _, member_id=member['id']: self.on_edit_member(member_id))
			delete_button.bind(on_release=lambda _, member_id=member['id']: self.on_delete_member(member_id))
			actions_layout.add_widget(edit_button)
			actions_layout.add_widget(delete_button)
			
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
	
	def on_edit_member(self, member_id):
		member_edit_screen = self.manager.get_screen('member_edit')
		member_edit_screen.member_id = member_id
		self.manager.current = 'member_edit'
		self.manager.transition = SlideTransition(direction="right")
	
	def on_delete_member(self, member_id):
		self.confirm_delete_member(member_id)
		
	def delete_member(self, member_id, popup):
		self.controller.delete_member(member_id)
		popup.dismiss()
		self.load()
		
	def confirm_delete_member(self, member_id):
		content = BoxLayout(orientation='vertical', padding=10, spacing=10)
		message = Label(text='Deseja realmente excluir o membro selecionado?')
		content.add_widget(message)
		buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
		confirm_button = Button(text='Confirmar', size_hint_x=None, width=dp(100))
		cancel_button = Button(text='Cancelar', size_hint_x=None, width=dp(100))
		buttons_layout.add_widget(confirm_button)
		buttons_layout.add_widget(cancel_button)
		content.add_widget(buttons_layout)
		popup = Popup(title='Excluir membro', content=content, size_hint=(0.5, 0.5))
		confirm_button.bind(on_release=lambda _: self.delete_member(member_id, popup))
		cancel_button.bind(on_release=popup.dismiss)
		popup.open()
	
	def on_back(self, *args):
		self.manager.transition.direction = "right"
		self.manager.current = "main"
