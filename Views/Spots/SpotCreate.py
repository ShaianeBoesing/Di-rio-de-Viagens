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
from kivy.uix.dropdown import DropDown
from Model.Category import Category
from Model.Member import Member
from kivy.uix.checkbox import CheckBox

#Precisa ser classe separada para ser chamado de outro ponto no sistema
class SpotCreate(Screen):
    def __init__(self, trip_controller: TripController, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = trip_controller

        #aqui é só a tela, mandar instancia para ctrl
        create_spot_layout = BoxLayout(orientation='vertical')

        #Título
        header_label = Label(text="Criação de spot", text_size=[800,600], font_size='30sp', halign='left', valign='middle')
        create_spot_layout.add_widget(header_label)

        #Nome
        name_box_layout = BoxLayout(orientation='vertical')
        name_label = Label(text="Nome do spot *", text_size=[800,600], font_size='16sp', halign='left', valign='middle')
        name_box_layout.add_widget(name_label)

        #truque para deixar input box menor
        spot_name_input_box = BoxLayout(orientation='vertical')
        spot_name_input = TextInput(multiline=False)
        spot_name_input_box.add_widget(spot_name_input)
        spot_name_input_box.add_widget(Label())

        name_box_layout.add_widget(spot_name_input_box)

        create_spot_layout.add_widget(name_box_layout)

        #Data e Hora
        horizontal_box_layout = BoxLayout()
        horizontal_box_layout.cols = 4

        start_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        start_hour_label = Label(text="Hora de início *", font_size='16sp',
                                 halign='center', valign='middle')

        start_hour_input = TextInput(multiline=False)

        start_hour_vertical_box_layout.add_widget(start_hour_label)
        start_hour_vertical_box_layout.add_widget(start_hour_input)

        end_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        end_hour_label = Label(text="Hora de fim *", font_size='16sp',
                                 halign='center', valign='middle')

        end_hour_input = TextInput(multiline=False)

        end_hour_vertical_box_layout.add_widget(end_hour_label)
        end_hour_vertical_box_layout.add_widget(end_hour_input)

        horizontal_box_layout.add_widget(start_hour_vertical_box_layout)
        horizontal_box_layout.add_widget(end_hour_vertical_box_layout)
        horizontal_box_layout.add_widget(Label())
        horizontal_box_layout.add_widget(Label())

        create_spot_layout.add_widget(horizontal_box_layout)

        #categoria_valor
        cv_horizontal_box_layout = BoxLayout()
        cv_horizontal_box_layout.cols = 4

        category_vertical_box_layout = BoxLayout(orientation='vertical')
        category_label = Label(text="Categoria *", font_size='16sp',
                                 halign='center', valign='middle')
        #TODO Na integração acessar traveller logado e pegar seu ID
        category_list = Category.list_by_traveller(1)

        dropdown_list = DropDown()
        for i in category_list:
            category_name = i.name
            text_string = category_name

            btn = Button(text=text_string, size_hint_y=None, height=50)
            btn.bind(on_press=lambda btn: dropdown_list.select(btn.text))

            dropdown_list.add_widget(btn)

        dropdown_list_button = Button()
        dropdown_list_button.bind(on_release=dropdown_list.open)

        dropdown_list.bind(on_select=lambda instance, x:
                           setattr(dropdown_list_button, 'text', x))

        #category_input = TextInput(multiline=False)
        #TODO colocar no parametro do callback de salvar

        category_vertical_box_layout.add_widget(category_label)
        category_vertical_box_layout.add_widget(dropdown_list_button)

        money_spent_vertical_box_layout = BoxLayout(orientation='vertical')
        money_spent_label = Label(text="Valor", font_size='16sp',
                                 halign='center', valign='middle')
        money_spent_input = TextInput(text="0,00", multiline=False)

        money_spent_vertical_box_layout.add_widget(money_spent_label)
        money_spent_vertical_box_layout.add_widget(money_spent_input)

        cv_horizontal_box_layout.add_widget(category_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(money_spent_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(Label())
        cv_horizontal_box_layout.add_widget(Label())

        create_spot_layout.add_widget(cv_horizontal_box_layout)

        #TODO Na integração acessar traveller e pegar membros
        bottom_horizontal_box_layout = BoxLayout()

        members_vertical_box = BoxLayout(orientation='vertical')
        members_label = Label(text="Membros", font_size='16sp',
                                 halign='center', valign='middle')

        members_check_box_placeholder = ScrollView()
        members_list = Member.list_by_traveller(1)

        members_list_output = []
        for member in members_list:
            line = BoxLayout()
            checkbox = CheckBox()
            #lógica complexa, existem 4 possiveis estados, apenas dois deles
            #entram no on_press, considerando que o botao comeca 'normal' e o
            #membro fora da lista
            checkbox.bind(on_press=lambda _, x=checkbox: members_list_output.append(member) if
                          (checkbox.state == 'down' and (member not in
                                                         members_list_output))
                          else members_list_output.remove(member))
            line.add_widget(checkbox)

            member_name = Label(text=member.name)
            line.add_widget(member_name)
            members_check_box_placeholder.add_widget(line)

        members_vertical_box.add_widget(members_label)
        members_vertical_box.add_widget(members_check_box_placeholder)

        save_button = Button(text='Salvar')
        return_button = Button(text='Voltar')

        bottom_horizontal_box_layout.add_widget(members_vertical_box)
        create_spot_layout.add_widget(bottom_horizontal_box_layout)

        self.add_widget(create_spot_layout)

    #talvez, se der tempo
    def show_calendar(self):
        pass

    def checkbox_on_active(self, checkbox, member):
        if checkbox.state == 'down':
            return member
        else:
            return None

