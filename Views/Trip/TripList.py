from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from Controllers.TripController import TripController


class TripList(Screen):
    def __init__(self, controller: TripController, **kwargs):
        super().__init__(**kwargs)
        self.trips = []
        self.controller = controller
        self.TEMP_TRAVELLER_ID = 1

    def on_pre_enter(self, *args):
        self.load()

    def load_categories(self):
        self.trips = self.controller.get_trips()

    def load(self):
        self.clear_widgets()  # Limpa todos os widgets da tela para não se sobrepor
        self.load_categories()  # Carrega o self.categories

        # Layout principal
        layout = BoxLayout(orientation='vertical')

        # Cabeçalho
        header_layout = BoxLayout(size_hint=(1, 0.1))
        subheader_layout = GridLayout(size_hint=(1, 0.1), cols=5)
        header_label = Label(text="Lista de Viagens", font_size='20sp', halign='center', valign='middle')
        header_label_title = Label(text="Titulo", font_size='20sp', halign='center', valign='middle')
        header_label_start = Label(text="Inicio", font_size='20sp', halign='center', valign='middle')
        header_label_end = Label(text="Fim", font_size='20sp', halign='center', valign='middle')
        header_label_actions = Label(text="Ações", font_size='20sp', halign='center', valign='middle',size_hint_x=None, width= 430)
        header_layout.add_widget(header_label)
        subheader_layout.add_widget(header_label_title)
        subheader_layout.add_widget(header_label_start)
        subheader_layout.add_widget(header_label_end)
        subheader_layout.add_widget(header_label_actions)
        layout.add_widget(header_layout)
        layout.add_widget(subheader_layout)
        # Tabela
        scrollview = ScrollView()
        table_layout = GridLayout(cols=4, size_hint_y=None, padding=(30, 50, 30, 50))
        table_layout.bind(minimum_height=table_layout.setter('height'))

        for trip in self.trips:
            title_label = Label(text=trip['title'], font_size='16sp', halign='center', valign='middle')
            start_date_label = Label(text=trip['start_date'], font_size='16sp', halign='center', valign='middle')
            end_date_label = Label(text=trip['end_date'], font_size='16sp', halign='center', valign='middle')

            # Layout para actions
            actions_layout = BoxLayout(size_hint_y=None, padding=10, size_hint=(None, None), size=(400, dp(40)),
                                       minimum_height=dp(40))
            actions_layout.cols = 2  # definir duas colunas
            actions_layout.col_default_width = 200  # definir largura da coluna como 200 pixels

            # Adiciona o nome à coluna 1 e actions_layout à coluna 2 do table_layout
            table_layout.add_widget(title_label)
            table_layout.add_widget(start_date_label)
            table_layout.add_widget(end_date_label)
            table_layout.add_widget(actions_layout)

            # Botão de actions
            see_button = Button(text="Ver", size_hint=(None, None), size=(200, dp(40)), font_size="16sp")
            see_button.bind(on_release=lambda _, trip_title=trip['title']: self.on_edit_trip(trip_title))
            edit_button = Button(text="Editar", size_hint=(None, None), size=(200, dp(40)), font_size="16sp")
            edit_button.bind(on_release=lambda _, trip_title=trip['title']: self.on_edit_trip(trip_title))
            actions_layout.add_widget(see_button)
            actions_layout.add_widget(edit_button)

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
        new_button.bind(on_release=self.on_new_trip)

    def on_new_trip(self, *args):
        self.manager.current = 'trip_create'
        self.manager.transition = SlideTransition(direction="left")

    def on_edit_trip(self, trip_title):
        trip_edit_screen = self.manager.get_screen('trip_edit')
        trip_edit_screen.trip_title = trip_title
        self.manager.current = 'trip_edit'
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
        self.manager.transition.direction = "right"
        self.manager.current = "main"
