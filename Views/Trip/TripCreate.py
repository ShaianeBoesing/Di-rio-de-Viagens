from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from Controllers.TripController import TripController
from kivy.uix.popup import Popup
from kivymd.uix.pickers import MDDatePicker
from datetime import date

class TripCreate(Screen):
    def __init__(self, controller: TripController, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = controller
        # self.date_picker = DatePicker()
        # Create the GridLayout for the register screen
        layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Add the "Registrar" label to the layout
        layout.add_widget(Label(text="Criar viagem"))

        # Create a GridLayout to hold the input fields
        input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
        layout.add_widget(input_grid)

        # Add the "Nome de Usuário" label and text input to the input grid
        input_grid.add_widget(Label(text="Titulo da viagem:"))
        self.title_input = TextInput()
        input_grid.add_widget(self.title_input)

        # Add the "Nome" label and text input to the input grid
        input_grid.add_widget(Label(text="Data de inicio:"))
        self.start_date = TextInput()
        input_grid.add_widget(self.start_date)

        # Add the "Senha" label and text input to the input grid
        input_grid.add_widget(Label(text="Data de fim:"))
        self.end_date = TextInput()
        input_grid.add_widget(self.end_date)

        # Create a GridLayout to hold the buttons
        button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
        layout.add_widget(button_grid)

        # Create the "Voltar" button and bind it to the on_return function
        return_button = Button(text="Voltar")
        return_button.bind(on_press=self.on_return)
        button_grid.add_widget(return_button)

        # Create the "Registrar" button and bind it to the on_register function
        register_button = Button(text="Registrar")
        register_button.bind(on_press=self.on_register)
        button_grid.add_widget(register_button)

        # Add the register layout to the screen
        self.add_widget(layout)

    def on_return(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "trip_list"

    def on_pre_enter(self, *args):
        self.title_input.text = ''
        self.start_date.text = ''
        self.end_date.text = ''

    def on_register(self, instance):
        title = self.title_input.text
        start_date = self.start_date.text
        end_date = self.end_date.text
        if len(title) == 0:
            self.show_popup("Erro ao criar viagem!", 'Titulo vazio!')
            return
        if (len(start_date)!=10) or (len(start_date.split('/')[2]) != 4 or len(start_date.split('/')[1]) != 2 or len(start_date.split('/')[0]) != 2):
            self.show_popup("Erro ao criar viagem!", 'Data de inicio no formato errado, formato esperado: AAAA/MM/DD')
            return
        if (len(end_date)!=10) or (len(end_date.split('/')[2]) != 4 or len(end_date.split('/')[1]) != 2 or len(end_date.split('/')[0]) != 2):
            self.show_popup("Erro ao criar viagem!", 'Data de fim no formato errado, formato esperado: AAAA/MM/DD')
            return
        try:
            start_date = date(int(start_date.split('/')[2]), int(start_date.split('/')[1]), int(start_date.split('/')[0]))
            end_date = date(int(end_date.split('/')[2]), int(end_date.split('/')[1]), int(end_date.split('/')[0]))
        except Exception:
            self.show_popup("Erro ao criar viagem!", 'Erro inesperado com as datas! ')
            return
        # Create a Popup with the Label as the content
        user_validation, message = self.trip_controller.create_trip(title, start_date, end_date)
        if user_validation:
            self.show_popup('Sucesso ao criar viajante!', message)
            self.title_input.text = ''
            self.start_date.text = ''
            self.end_date.text = ''
            self.manager.transition.direction = "right"
            self.manager.current = "trip_list"
        else:
            self.show_popup("Erro ao criar viajante!", message)



    def show_popup(self, title, text):
        popup = Popup(title=title, size_hint=(None, None), size=(625, 200))
        layout = GridLayout(cols=1, spacing=10, padding=10)
        layout.add_widget(Label(text=text))
        btn = Button(text="voltar", size_hint=(1, None), height=50)
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.add_widget(layout)
        popup.open()

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            min_date=date(2021, 2, 15),
            max_date=date(2021, 3, 27),
        )
        date_dialog.open()