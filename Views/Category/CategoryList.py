from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from Controllers.CategoryController import CategoryController

class CategoryList(Screen):
	def __init__(self, controller: CategoryController, my_app_instance, **kwargs):
		super().__init__(**kwargs)
		self.categories = []
		self.controller = controller
		self.my_app_instance = my_app_instance

	def on_pre_enter(self, *args):
		self.load()
	
	def load_categories(self):
		self.categories = self.controller.list_categories_by_traveller(self.my_app_instance.traveller_id)
	
	def load(self):
		self.clear_widgets() # Limpa todos os widgets da tela para não se sobrepor
		self.load_categories() # Carrega o self.categories
		
		# Layout principal
		layout = BoxLayout(orientation='vertical')
		
		# Cabeçalho
		header_layout = BoxLayout(size_hint=(1, 0.1))
		header_label = Label(text="Lista de Categorias", font_size='20sp', halign='center', valign='middle')
		header_layout.add_widget(header_label)
		layout.add_widget(header_layout)
		
		# Tabela
		scrollview = ScrollView()
		table_layout = GridLayout(cols=2, size_hint_y=None, padding=(30, 50, 30, 50))
		table_layout.bind(minimum_height=table_layout.setter('height'))
		
		for category in self.categories:
			name_label = Label(text=category['name'], font_size='16sp', halign='center', valign='middle')
			
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
			edit_button.bind(on_release=lambda _, category_id=category['id']: self.on_edit_category(category_id))
			delete_button.bind(on_release=lambda _, category_id=category['id']: self.on_delete_category(category_id))
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
		new_button.bind(on_release=self.on_new_category)
	
	def on_new_category(self, *args):
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = 'category_create'

	def on_edit_category(self, category_id):
		category_edit_screen = self.manager.get_screen('category_edit')
		category_edit_screen.category_id = category_id
		self.manager.current = 'category_edit'
		self.manager.transition = SlideTransition(direction="right")
	
	def on_delete_category(self, category_id):
		self.confirm_delete_category(category_id)
		
	def delete_category(self, category_id, popup):
		self.controller.delete_category(category_id)
		popup.dismiss()
		self.load()
		
	def confirm_delete_category(self, category_id):
		content = BoxLayout(orientation='vertical', padding=10, spacing=10)
		message = Label(text='Deseja realmente excluir o Categoria selecionada?')
		content.add_widget(message)
		buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
		confirm_button = Button(text='Confirmar', size_hint_x=None, width=dp(100))
		cancel_button = Button(text='Cancelar', size_hint_x=None, width=dp(100))
		buttons_layout.add_widget(confirm_button)
		buttons_layout.add_widget(cancel_button)
		content.add_widget(buttons_layout)
		popup = Popup(title='Excluir Categoria', content=content, size_hint=(0.5, 0.5))
		confirm_button.bind(on_release=lambda _: self.delete_category(category_id, popup))
		cancel_button.bind(on_release=popup.dismiss)
		popup.open()
	
	def on_back(self, *args):
		self.manager.transition.direction = "down"
		self.manager.current = "trip_list"
