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
from datetime import datetime

#Precisa ser classe separada para ser chamado de outro ponto no sistema
class SpotCreate(Screen):
    def __init__(self, trip_controller: TripController, my_app_instance, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = trip_controller
        self.my_app_instance = my_app_instance

    def on_pre_enter(self):
        self.clear_widgets()
        #self.load_spots()
        self.on_create_spot()

    '''
    def load_spots(self):
        self.trip_controller.spots = self.trip_controller.get_spots(self.my_app_instance.traveller_id)
    '''

    def on_create_spot(self):
        self.clear_widgets()
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
        horizontal_box_layout.cols = 3

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
        ###
        start_date_vertical_box_layout = BoxLayout(orientation='vertical')
        start_date_label = Label(text="Data *", font_size='16sp',
                                 halign='center', valign='middle')

        start_date_input = TextInput(multiline=False)

        start_date_vertical_box_layout.add_widget(start_date_label)
        start_date_vertical_box_layout.add_widget(start_date_input)

        ###

        end_hour_vertical_box_layout.add_widget(end_hour_label)
        end_hour_vertical_box_layout.add_widget(end_hour_input)

        horizontal_box_layout.add_widget(start_hour_vertical_box_layout)
        horizontal_box_layout.add_widget(end_hour_vertical_box_layout)
        horizontal_box_layout.add_widget(start_date_vertical_box_layout)
        horizontal_box_layout.add_widget(Label())
        horizontal_box_layout.add_widget(Label())
        horizontal_box_layout.add_widget(Label())

        create_spot_layout.add_widget(horizontal_box_layout)

        #categoria_valor
        cv_horizontal_box_layout = BoxLayout()
        cv_horizontal_box_layout.cols = 4

        category_vertical_box_layout = BoxLayout(orientation='vertical')
        category_label = Label(text="Categoria *", font_size='16sp',
                                 halign='center', valign='middle')

        category_list = Category.list_by_traveller(self.my_app_instance.traveller_id)

        dropdown_list = DropDown()
        choosen_category = [None]
        for i in category_list:
            category_name = i.name
            text_string = category_name

            btn = Button(text=text_string, size_hint_y=None, height=50)
            btn.bind(on_press=lambda btn:
                     [dropdown_list.select(btn.text),
                      choosen_category.pop(),
                      choosen_category.insert(0, i)])

            dropdown_list.add_widget(btn)

        dropdown_list_button = Button()
        dropdown_list_button.bind(on_release=dropdown_list.open)

        dropdown_list.bind(on_select=lambda instance, x:
                           setattr(dropdown_list_button, 'text', x))

        category_vertical_box_layout.add_widget(category_label)
        category_vertical_box_layout.add_widget(dropdown_list_button)

        money_spent_vertical_box_layout = BoxLayout(orientation='vertical')
        money_spent_label = Label(text="Valor", font_size='16sp',
                                 halign='center', valign='middle')
        money_spent_input = TextInput(text="0,00", multiline=False)

        money_spent_vertical_box_layout.add_widget(money_spent_label)
        money_spent_vertical_box_layout.add_widget(money_spent_input)


        #rating
        rating_box_layout = BoxLayout(orientation='vertical')
        rating_label = Label(text="Avaliação", font_size='16sp',
                                  halign='center', valign='middle')
        rating_input = TextInput(multiline=False)

        rating_box_layout.add_widget(rating_label)
        rating_box_layout.add_widget(rating_input)

        cv_horizontal_box_layout.add_widget(category_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(money_spent_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(rating_box_layout)
        cv_horizontal_box_layout.add_widget(Label())
        cv_horizontal_box_layout.add_widget(Label())

        create_spot_layout.add_widget(cv_horizontal_box_layout)

        bottom_horizontal_box_layout = BoxLayout()

        members_vertical_box = BoxLayout(orientation='vertical')
        members_label = Label(text="Membros", font_size='16sp',
                                 halign='center', valign='middle')

        members_check_box_placeholder = ScrollView()

        table_layout = GridLayout(cols=1, row_default_height=30, size_hint_y=None, padding=(30, 50, 30, 50))
        table_layout.bind(minimum_height=table_layout.setter('height'))

        members_list = Member.list_by_traveller(self.my_app_instance.traveller_id)

        members_list_output = []
        for member in members_list:
            line = BoxLayout()
            checkbox = CheckBox()

            #basicamente um if, elif, else, só que tem que ser tudo em lambda
            checkbox.bind(on_press=lambda _, x=member:
                          members_list_output.append(x) if
                          self.checkbox_append_check(checkbox.state, x,
                                               members_list_output) else
                          (members_list_output.remove(self.checkbox_find_equivalent(x, members_list_output)) if
                           self.checkbox_remove_check(checkbox.state, x,
                                                      members_list_output) else
                           True==True))

            line.add_widget(checkbox)

            member_name = Label(text=member.name)
            line.add_widget(member_name)
            table_layout.add_widget(line)

        members_check_box_placeholder.add_widget(table_layout)

        members_vertical_box.add_widget(members_label)
        members_vertical_box.add_widget(members_check_box_placeholder)

        save_button_box_layout = BoxLayout(orientation='vertical')
        save_button = Button(text='Salvar', font_size='18sp')
        save_button.bind(on_press=lambda _, x=[spot_name_input,
                                               start_hour_input,
                                               end_hour_input,
                                               choosen_category,
                                               money_spent_input,
                                               members_list_output,
                                               start_date_input,
                                               rating_input]:
                         self.on_save_option(x))

        save_button_box_layout.add_widget(Label())
        save_button_box_layout.add_widget(save_button)

        return_button_box_layout = BoxLayout(orientation='vertical')
        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_return_option)

        return_button_box_layout.add_widget(Label())
        return_button_box_layout.add_widget(return_button)

        bottom_horizontal_box_layout.add_widget(members_vertical_box)
        bottom_horizontal_box_layout.add_widget(Label())
        bottom_horizontal_box_layout.add_widget(save_button_box_layout)
        bottom_horizontal_box_layout.add_widget(return_button_box_layout)

        create_spot_layout.add_widget(bottom_horizontal_box_layout)

        self.add_widget(create_spot_layout)

    def checkbox_check(self, checkbox, member):
        if checkbox.state == 'down':
            return member
        else:
            return None

    def on_return_option(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "spot_view"

    def on_save_option(self, arguments_list):
        #string não pode ser vazia
        name_field = self.check_name_field(arguments_list[0].text)
        if name_field is None:
            self.show_popup('Erro Nome','Campo nome não preenchido')
            return

        #testes de campo de data de início
        start_hour_datetime = self.check_time_field(arguments_list[1].text)
        if start_hour_datetime is None:
            self.show_popup('Erro hora de início',
                            'A hora deve estar no formato \"HH:MM\"')
            # 'A data e hora deve estar no formato \"AAAA-MM-DD HH:MM:SS\"')
            return
        else:
            start_hour_datetime = start_hour_datetime + ':00'

        spot_rating = self.check_name_field(arguments_list[7].text)
        try:
            if not 0 <= int(spot_rating) <= 5:
                self.show_popup('Erro na avaliação', 'A avaliação deve ser um numero entre 0 a 5')
                return
        except Exception as e:
            print(e)
            self.show_popup('Erro na avaliação',
                            'Ocorreu algum erro inesperado, a avaliação deve ser um numero entre 0 a 5')
            return

        #testes de campo de data de fim
        end_hour_datetime = self.check_time_field(arguments_list[2].text)
        if end_hour_datetime is None:
            self.show_popup('Erro hora de fim',
                            'A hora deve estar no formato \"HH:MM\"')
            return
        else:
            end_hour_datetime = end_hour_datetime + ':00'

        # testes de campo de data
        start_date = arguments_list[6].text
        if (len(start_date)!=10) or (len(start_date.split('/')[2]) != 4 or len(start_date.split('/')[1]) != 2 or len(start_date.split('/')[0]) != 2):
            self.show_popup('Erro data',
                            'A data deve estar no formato \"DD/MM/AAAA\"')
            return
        else:
            start_date = f'{(start_date.split("/")[2])}-{(start_date.split("/")[1])}-{(start_date.split("/")[0])}'

        #checar se hora de início é maior que hora fim 
        if start_hour_datetime >= end_hour_datetime:
            self.show_popup('Erro Data e hora',
                            'A data e hora do fim não podem ser menores que os do início')
            return

        #checar se alguma categoria foi selecionada
        category_object = self.check_category_field(arguments_list[3])
        if category_object is None:
            self.show_popup('Erro Categoria',
                            'Selecione pelo menos uma categoria')
            return

        #checar valor dinheiro
        money_float = self.check_money_spent_field(arguments_list[4].text)
        if money_float is None:
            self.show_popup('Erro Dinheiro gasto',
                            'O campo de dinheiro deve estar no formato \"XX,XX\"')
            return

        #checar membros é no controller print(arguments_list[5]) membros
        spot_members_list = arguments_list[5]
        create_spot_validation, message = self.trip_controller.create_spot(name_field,
                                                                           money_float,
                                                                           (start_date + ' ' + start_hour_datetime),
                                                                           (start_date + ' ' + end_hour_datetime),
                                                                           category_object,
                                                                           spot_members_list,
                                                                           self.my_app_instance.traveller_id,
                                                                           spot_rating)
        if not(create_spot_validation):
            self.show_popup('Erro', message)
        else:
            self.show_popup('Spot criado', message)
            self.on_return_trip()

    def on_return_trip(self):
        self.manager.transition.direction = "left"
        self.manager.current = "spot_view"

    def checkbox_remove_check(self, checkbox_state, member, member_list):
        if checkbox_state == 'normal':
            if member.id in [j.id for j in member_list]:
                return True
            else:
                return False
        return False

    def checkbox_append_check(self, checkbox_state, member, member_list):
        if checkbox_state == 'down':
            if member.id not in [j.id for j in member_list]:
                return True
            else:
                return False
        return False

    def checkbox_find_equivalent(self, member, member_list):
        for i in member_list:
            if i.id == member.id:
                return i

    def show_popup(self, title: str, text: str, button_text="Voltar"):
        popup = Popup(title=title, size_hint=(None, None), size=(500, 200))
        layout = GridLayout(cols=1, spacing=10, padding=10)
        layout.add_widget(Label(text=text))
        btn = Button(text=button_text, size_hint=(1, None), height=50)
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.add_widget(layout)
        popup.open()

    def check_name_field(self, name_field: str):
        name_field = name_field.strip()
        if len(name_field) <= 0:
            return None
        else:
            return name_field

    def check_time_field(self, time_field: str):
        try:
            if (len(time_field)!=5) or (len(time_field.split(':')[0]) != 2 or len(time_field.split(':')[1]) != 2):
                int(time_field.split(':'[0]))
                int(time_field.split(':'[1]))
                raise Exception
        except Exception:
            return None
        else:
            return time_field

    def check_category_field(self, category_field: list):
        if category_field[0] is None:
            return None
        else:
            return category_field[0]

    def check_money_spent_field(self, money_spent_field: str):
        try:
            money_spent_field = money_spent_field.strip()
            money_spent_field = money_spent_field.replace(',','.')
            money_float = float(money_spent_field)
        except:
            return None
        else:
            return money_float

