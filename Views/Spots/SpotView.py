from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from Controllers.TripController import TripController
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

class SpotView(Screen):
    def __init__(self, trip_controller: TripController, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = trip_controller
        self.layout = None
        self.on_list_spots()
        '''
        if first_screen_option == 'list_spots_screen':
            self.on_list_spots()
        elif first_screen_option == 'create_spot_option':
            self.on_create_spot_option()
        '''

    def on_list_spots(self):
        spots = self.trip_controller.get_spots()
        self.clear_widgets()

        list_spot_layout = BoxLayout(orientation='vertical')

        # Cabeçalho
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_label = Label(text="Lista de spots", font_size='20sp', halign='center', valign='middle')
        header_layout.add_widget(header_label)
        list_spot_layout.add_widget(header_layout)

        # Tabela
        scrollview = ScrollView()
        table_layout = GridLayout(cols=3, size_hint_y=None, padding=(30, 50, 30, 50))
        table_layout.bind(minimum_height=table_layout.setter('height'))

        for spot in spots:
            name_label = Label(text=spot.name, font_size='16sp', halign='center', valign='middle')
            status_label = Label(text=spot.status, font_size='16sp', halign='center', valign='middle')

            # Layout para actions
            ##size é importante se quiser add mais elementos
            actions_layout = BoxLayout(size_hint_y=None, padding=10, size_hint=(None, None), size=(400, dp(40)), minimum_height=dp(40))
            actions_layout.cols = 3  # definir duas colunas
            actions_layout.col_default_width = 200  # definir largura da coluna como 200 pixels

            # Adiciona o nome à coluna 1 e actions_layout à coluna 2 do table_layout
            table_layout.add_widget(name_label)
            table_layout.add_widget(status_label)
            table_layout.add_widget(actions_layout)

            # Botão de actions
            view_spot = Button(text="Ver", size_hint=(None, None), size=(100, dp(40)), font_size="16sp")
            update_spot = Button(text="Editar", size_hint=(None, None), size=(100, dp(40)), font_size="16sp")
            delete_spot = Button(text="Excluir", size_hint=(None, None), size=(100, dp(40)), font_size="16sp")
            view_spot.bind(on_release=lambda _, spot_object=spot:
                           self.on_view_spot_option(spot_object))
            update_spot.bind(on_release=lambda _, spot_object=spot:
                             self.on_update_spot_option(spot_object))
            delete_spot.bind(on_release=lambda _, spot_object=spot:
                             self.on_delete_spot_option(spot_object))
            actions_layout.add_widget(view_spot)
            actions_layout.add_widget(update_spot)
            actions_layout.add_widget(delete_spot)

        scrollview.add_widget(table_layout)
        list_spot_layout.add_widget(scrollview)

        # Botao
        buttons_layout = BoxLayout(size_hint=(1, 0.1), padding=10)
        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_return_trip)
        buttons_layout.add_widget(return_button)
        list_spot_layout.add_widget(buttons_layout)

        self.add_widget(list_spot_layout)


    def on_return_trip(self):
        pass

    def on_view_spot_option(self, spot):
        self.clear_widgets()

    def on_update_spot_option(self, spot):
        pass

    def on_delete_spot_option(self, spot):
        pass

