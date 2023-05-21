from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainView(Screen):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.name = "main"

        # Create the GridLayout for the main screen
        layout = GridLayout(cols=1, padding=(30, 50, 30, 50))

        # Add the image to the layout
        layout.add_widget(Image(source="Views/Images/diario.png", size_hint_y=0.5))

        # Add the "Enter or Register" label to the layout
        layout.add_widget(Label(text="Entre ou Registre-se"))

        # Create a GridLayout to hold the Login and Register buttons
        button_grid = GridLayout(cols=2, size_hint_y=0.2, size=layout.size)
        layout.add_widget(button_grid)

        # Add the Login button to the button grid
        login_button = Button(text="Entrar")
        login_button.bind(on_press=self.go_to_login)
        button_grid.add_widget(login_button)

        # Add the Register button to the button grid
        register_button = Button(text="Registrar")
        register_button.bind(on_press=self.go_to_register)
        button_grid.add_widget(register_button)

        # Add the Member button to the button grid
        member_button = Button(text="Membros")
        member_button.bind(on_press=self.go_to_members)
        button_grid.add_widget(member_button)

        # Add the Member button to the button grid
        category_button = Button(text="Categorias")
        category_button.bind(on_press=self.go_to_categories)
        button_grid.add_widget(category_button)

        # Add the main layout to the screen
        self.add_widget(layout)

    def go_to_register(self, instance):
        # Switch to the "register" screen
        self.manager.transition.direction = "left"
        self.manager.current = "register_view"

    def go_to_members(self, instance):
        # Switch to the "register" screen
        self.manager.transition.direction = "left"
        self.manager.current = "member_list"

    def go_to_categories(self, instance):
        # Switch to the "register" screen
        self.manager.transition.direction = "left"
        self.manager.current = "category_list"
    
    def go_to_login(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "login_view"

