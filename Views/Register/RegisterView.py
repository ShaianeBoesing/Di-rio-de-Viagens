from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from Controllers.UserController import UserController
from kivy.uix.popup import Popup


class RegisterView(Screen):
    def __init__(self, controller:UserController, **kwargs):
        super().__init__(**kwargs)
        self.user_contoller = controller
        # Create the GridLayout for the register screen
        layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Add the "Registrar" label to the layout
        layout.add_widget(Label(text="Registrar"))

        # Create a GridLayout to hold the input fields
        input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
        layout.add_widget(input_grid)

        # Add the "Nome de Usuário" label and text input to the input grid
        input_grid.add_widget(Label(text="Nome de Usuário:"))
        self.username_input = TextInput()
        input_grid.add_widget(self.username_input)

        # Add the "Nome" label and text input to the input grid
        input_grid.add_widget(Label(text="Nome:"))
        self.name_input = TextInput()
        input_grid.add_widget(self.name_input)

        # Add the "Senha" label and text input to the input grid
        input_grid.add_widget(Label(text="Senha:"))
        self.password_input = TextInput(password=True)
        input_grid.add_widget(self.password_input)

        # Add the "Confirmar Senha" label and text input to the input grid
        input_grid.add_widget(Label(text="Confirmar Senha:"))
        self.confirm_password_input = TextInput(password=True)
        input_grid.add_widget(self.confirm_password_input)

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
        self.manager.current = "main"

    def on_register(self, instance):
        username = self.username_input.text
        name = self.name_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        # Create a Popup with the Label as the content
        user_validation, message = self.user_contoller.register_user(username, name, password,confirm_password)
        if user_validation:
            self.show_popup('Sucesso ao criar viajante!', message)
            self.username_input.text = ''
            self.name_input.text = ''
            self.password_input.text = ''
            self.password_input.text = ''
            self.confirm_password_input.text = ''
            self.manager.transition.direction = "left"
            self.manager.current = "main"
        else:
            self.show_popup("Erro ao criar viajante!", message)



    def show_popup(self, title, text):
        popup = Popup(title=title, size_hint=(None, None), size=(425, 200))
        layout = GridLayout(cols=1, spacing=10, padding=10)
        layout.add_widget(Label(text=text))
        btn = Button(text="voltar", size_hint=(1, None), height=50)
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.add_widget(layout)
        popup.open()