from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from Controllers.UserController import UserController
from kivy.uix.popup import Popup

#TODO alterar on_login
#show_popup e on_return ficam identicos, porem nao fazemos herança dupla

class LoginView(Screen):
    def __init__(self, controller:UserController, **kwargs):
        super().__init__(**kwargs)
        self.user_contoller = controller

        layout = GridLayout(cols=1, padding=(30, 50, 30, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(Label(text="Entrar"))

        # Create a GridLayout to hold the input fields
        input_grid = GridLayout(cols=2, size_hint_y=0.6, size=layout.size, padding=(0, 0, 0, 50))
        layout.add_widget(input_grid)

        # Add the "Nome de Usuário" label and text input to the input grid
        input_grid.add_widget(Label(text="Nome de Usuário: *"))
        self.username_input = TextInput(multiline=False)
        input_grid.add_widget(self.username_input)

        input_grid.add_widget(Label(text="Senha: *"))
        self.password_input = TextInput(multiline=False, password=True)
        input_grid.add_widget(self.password_input)

        # Create a GridLayout to hold the buttons
        button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
        layout.add_widget(button_grid)

        return_button = Button(text="Voltar")
        return_button.bind(on_press=self.on_return)
        button_grid.add_widget(return_button)

        login_button = Button(text="Entrar")
        login_button.bind(on_press=self.on_login)
        button_grid.add_widget(login_button)

        self.add_widget(layout)

    def on_return(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

    def on_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        user_validation, message = self.user_contoller.login(username, password)
        if user_validation:
            self.show_popup('Entrou', message, 'Confirmar')
            self.username_input.text = ''
            self.password_input.text = ''

            #TODO Aqui vai futuramente transicionar a futura tela do sistema já logado
            self.manager.transition.direction = "left"
            self.manager.current = "main"
        else:
            self.show_popup("Erro ao entrar!", message)
            self.password_input.text = ''

    def show_popup(self, title: str, text: str, button_text="voltar"):
        popup = Popup(title=title, size_hint=(None, None), size=(425, 200))
        layout = GridLayout(cols=1, spacing=10, padding=10)
        layout.add_widget(Label(text=text))
        btn = Button(text=button_text, size_hint=(1, None), height=50)
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.add_widget(layout)
        popup.open()

