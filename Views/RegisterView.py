import PySimpleGUI as sg

from Controllers.UserController import UserController


class RegisterView:
    def __init__(self):
        # Define the layout of the window
        layout = [
            [sg.Text('Criar conta', size=(40, 1), justification='center', font=("Helvetica", 25))],
            [sg.Text('Nome de usuário:', size=(15, 1)), sg.InputText(key='username')],
            [sg.Text('Nome:', size=(15, 1)), sg.InputText(key='name')],
            [sg.Text('Senha', size=(15, 1)), sg.InputText(key='password', password_char='*')],
            [sg.Text('Confirmar senha', size=(15, 1)), sg.InputText(key='confirm_password', password_char='*')],
            [sg.Button('Registrar', key='register_button'), sg.Button('Cancelar', key='cancel_button')]
        ]

        self.window = sg.Window('Diario de viagens').Layout(layout)

        self.user_controller = UserController()

    def show(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'cancel_button':
                # Close the window if the user clicks the Cancel button or closes the window
                break
            elif event == 'register_button':
                # Get the values from the inputs
                username = values['username']
                name = values['name']
                password = values['password']
                confirm_password = values['confirm_password']

                if password != confirm_password:
                    # Show an error message if the passwords don't match
                    sg.popup('Error: The passwords do not match')
                else:
                    # Create a UserController instance and register the user
                    controller = UserController()
                    if controller.register_user(username, name, password):
                        # Show a success message and close the window if the registration is successful
                        sg.popup('Registration successful')
                        break
                    else:
                        # Show an error message if the username is already taken
                        sg.popup('Error: The username is already taken')

        self.window.close()