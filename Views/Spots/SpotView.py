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
#from Model.Category import Category

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

    def on_list_spots(self, *args):
        #TODO na integração possivelmente bastará pegar o atributo spots da trip
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
        buttons_layout.add_widget(Label())

        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_return_trip)
        buttons_layout.add_widget(return_button)
        list_spot_layout.add_widget(buttons_layout)

        self.add_widget(list_spot_layout)


    def on_return_trip(self, *args):
        self.clear_widgets()

    def on_view_spot_option(self, spot):
        self.clear_widgets()
        view_spot_layout = BoxLayout(orientation='vertical')

        # Título
        header_label = Label(text=spot.name, text_size=self.size, font_size='30sp', halign='left', valign='middle')
        view_spot_layout.add_widget(header_label)

        name_box_layout = BoxLayout(orientation='vertical')
        # Nome do spot label
        name_label = Label(text="Nome do spot", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        name_box_layout.add_widget(name_label)

        # Nome do spot
        name = Label(text=spot.name, text_size=self.size, font_size='18sp', halign='left', valign='middle')
        name_box_layout.add_widget(name)
        view_spot_layout.add_widget(name_box_layout)

        #dentro desse boxlayout horizontal eu tenho 3 boxlayout verticais
        '''
        status_horizontal_box_layout = BoxLayout(size_hint_y=None,
                                                 size_hint=(None, None),
                                                     size=(800, dp(50)), minimum_height=dp(40))
        '''
        status_horizontal_box_layout = BoxLayout(size_hint_y=None,
                                                 size_hint=(1.0,1.0))
        status_horizontal_box_layout.cols = 3
        status_horizontal_box_layout.col_default_width = 200

        #status_horizontal_box_layout.add_widget(Label())

        start_hour_vertical_box_layout = BoxLayout(orientation='vertical', )
        start_hour_label = Label(text="Hora de início", text_size=self.size,
                                 size=(100, dp(40)), bold=True,
                                 font_size='16sp', halign='center',
                                 valign='middle')
        start_hour = Label(text=spot.start_hour, text_size=self.size,
                           size=(100, dp(40)),
                           font_size='18sp', halign='center', valign='middle')
        start_hour_vertical_box_layout.add_widget(start_hour_label)
        start_hour_vertical_box_layout.add_widget(start_hour)

        end_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        end_hour_label = Label(text="Hora de fim", text_size=self.size,
                               size=(100, dp(40)), bold=True,
                               font_size='16sp', halign='center', valign='middle')
        end_hour = Label(text=spot.end_hour, text_size=self.size,
                         size=(100, dp(40)),
                         font_size='18sp', halign='center', valign='middle')
        end_hour_vertical_box_layout.add_widget(end_hour_label)
        end_hour_vertical_box_layout.add_widget(end_hour)

        spot_status_vertical_box_layout = BoxLayout(orientation='vertical')
        spot_status_label = Label(text="Status", text_size=self.size,
                                  size=(100, dp(40)), bold=True,
                                  font_size='16sp', halign='center', valign='middle')
        spot_status = Label(text=spot.status, text_size=self.size,
                            size=(100, dp(40)),
                            font_size='18sp', halign='center', valign='middle')
        spot_status_vertical_box_layout.add_widget(spot_status_label)
        spot_status_vertical_box_layout.add_widget(spot_status)

        status_horizontal_box_layout.add_widget(start_hour_vertical_box_layout)
        status_horizontal_box_layout.add_widget(end_hour_vertical_box_layout)
        status_horizontal_box_layout.add_widget(spot_status_vertical_box_layout)

        view_spot_layout.add_widget(status_horizontal_box_layout)

        categoria_box_layout = BoxLayout(orientation='vertical')
        #categoria_label
        categoria_label = Label(text="Categoria", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        categoria_box_layout.add_widget(categoria_label)

        #categoria
        categoria = Label(text=spot.category.name, text_size=self.size, font_size='18sp', halign='left', valign='middle')
        categoria_box_layout.add_widget(categoria)
        view_spot_layout.add_widget(categoria_box_layout)

        members_string = ""
        for member in spot.members:
            members_string += member.name + ", "
        members_string = members_string[:-2]

        membros_box_layout = BoxLayout(orientation='vertical')
        #membros_label
        membros_label = Label(text="Membros", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        membros_box_layout.add_widget(membros_label)

        #membros
        membros = Label(text=members_string, text_size=self.size, font_size='18sp', halign='left', valign='middle')
        membros_box_layout.add_widget(membros)
        view_spot_layout.add_widget(membros_box_layout)

        #valor_gasto
        valor_box_layout = BoxLayout(orientation='vertical')
        #valor_label
        valor_label = Label(text="Valor", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        valor_box_layout.add_widget(valor_label)

        #valor
        valor = Label(text=str(spot.money_spent), text_size=self.size, font_size='18sp', halign='left', valign='middle')
        valor_box_layout.add_widget(valor)
        view_spot_layout.add_widget(valor_box_layout)

        #Botao
        button_box_layout = BoxLayout(size_hint=(1.0,0.5), padding=10)
        button_box_layout.add_widget(Label())

        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_list_spots)
        button_box_layout.add_widget(return_button)

        view_spot_layout.add_widget(button_box_layout)

        self.add_widget(view_spot_layout)

    def on_update_spot_option(self, spot):
        self.clear_widgets()

    def on_delete_spot_option(self, spot):
        self.clear_widgets()

