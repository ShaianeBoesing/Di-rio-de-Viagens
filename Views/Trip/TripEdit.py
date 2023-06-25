from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from Controllers.TripController import TripController
from kivy.uix.popup import Popup
from datetime import date
from kivy.metrics import dp


class TripEdit(Screen):
    def __init__(self, controller: TripController, my_app_instance, trip_tile=None, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = controller
        self.trip_title = trip_tile
        self.my_app_instance = my_app_instance
        # self.date_picker = DatePicker()
        # Create the GridLayout for the register screen
        layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Add the "Registrar" label to the layout
        layout.add_widget(Label(text=f"Editar viagem"))

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

        input_grid.add_widget(Label(text="Status:"))
        self.status = TextInput()
        input_grid.add_widget(self.status)

        # Create a GridLayout to hold the buttons
        button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
        layout.add_widget(button_grid)

        # Create the "Voltar" button and bind it to the on_return function
        return_button = Button(text="Voltar")
        return_button.bind(on_press=self.on_return)
        button_grid.add_widget(return_button)

        # Create the "Registrar" button and bind it to the on_register function
        register_button = Button(text="Editar")
        register_button.bind(on_press=self.on_edit)
        button_grid.add_widget(register_button)

        register_button = Button(text="Excluir")
        register_button.bind(on_press=self.on_delete_member)
        button_grid.add_widget(register_button)

        # Add the register layout to the screen
        self.add_widget(layout)

    def on_return(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "trip_list"

    def on_pre_enter(self, *args):
        if self.trip_title is not None:
            attributes = self.trip_controller.get_trip(self.trip_title)
            start_date_month = str(attributes['start_date'].month) if len(str(attributes['start_date'].month)) == 2 else '0' + str(attributes['start_date'].month)
            start_date_day = str(attributes['start_date'].day) if len(str(attributes['start_date'].day)) == 2 else '0' + str(attributes['start_date'].day)
            end_date_month = str(attributes['end_date'].month) if len(str(attributes['end_date'].month)) == 2 else '0' + str(attributes['end_date'].month)
            end_date_day = str(attributes['end_date'].day) if len(str(attributes['end_date'].day)) == 2 else '0' + str(attributes['end_date'].day)
            self.title_input.text = attributes['title']
            self.start_date.text = start_date_day + '/' + start_date_month+'/' + str(attributes['start_date'].year )
            self.end_date.text = end_date_day+'/'+end_date_month+'/'+str(attributes['end_date'].year)
            self.status.text = attributes['status']

    def on_edit(self, instance):
        title = self.title_input.text
        start_date = self.start_date.text
        end_date = self.end_date.text
        status = self.status.text
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
        user_validation, message = self.trip_controller.edit_trip(self.trip_title, {'title':title,'start_date':start_date,'end_date':end_date,'status':status}, self.my_app_instance.traveller_id)
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

    def on_delete_member(self, trip_title):
        self.confirm_delete_trip(self.trip_title)

    def delete_member(self, trip_title, popup):
        self.trip_controller.delete_trip(trip_title, self.my_app_instance.traveller_id)
        popup.dismiss()
        self.on_return(self)

    def confirm_delete_trip(self, trip_title):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        message = Label(text='Deseja realmente excluir a viagem?')
        content.add_widget(message)
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=10)
        confirm_button = Button(text='Confirmar', size_hint_x=None, width=dp(100))
        cancel_button = Button(text='Cancelar', size_hint_x=None, width=dp(100))
        buttons_layout.add_widget(confirm_button)
        buttons_layout.add_widget(cancel_button)
        content.add_widget(buttons_layout)
        popup = Popup(title='Excluir viagem', content=content, size_hint=(0.5, 0.5))
        confirm_button.bind(on_release=lambda _: self.delete_member(trip_title, popup))
        cancel_button.bind(on_release=popup.dismiss)
        popup.open()