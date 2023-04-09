import PySimpleGUI as sg

from Views.RegisterView import RegisterView


class MainView:
    def __init__(self):
        # Define the layout of the window
        layout = [
            [sg.Text('Diário de Viagens', font=('Arial', 40), justification='center')],
            [sg.Column([[sg.Button('Entrar', key='login_button', size=(10, 2)), sg.Button('Registrar', key='register_button', size=(10, 2))]], justification='center')],
        ]
        self.window = sg.Window('Diario de Viagens', layout)

    def show(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                # Close the window if the user closes the window
                break
            elif event == 'register_button':
                # Open the RegisterView if the user clicks the Register button
                RegisterView().show()
            elif event == 'login_button':
                # TODO: Implement the LoginView
                sg.popup('Login not implemented yet')

        self.window.close()
