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
from kivy.uix.checkbox import CheckBox
from Model.Category import Category
from Model.Member import Member
from datetime import datetime

class SpotView(Screen):
    def __init__(self, trip_controller: TripController, my_app_instance, **kwargs):
        super().__init__(**kwargs)
        self.trip_controller = trip_controller
        self.layout = None
        self.my_app_instance = my_app_instance
        #self.on_pre_enter()

    def on_pre_enter(self):
        self.clear_widgets()
        #self.load_spots()
        current_trip = self.trip_controller.current_trip
        if current_trip != None:
            finished_trip_check_bool = self.trip_controller.finished_trip_check()
            if finished_trip_check_bool:
                self.trip_controller.cancel_all_spots()

        self.on_list_spots()

    '''
    def load_spots(self):
        current_trip = self.trip_controller.current_trip
        if current_trip == None:
            return
        #self.trip_controller.spots = self.trip_controller.get_spots(self.trip_controller.current_trip)
    '''

    def on_list_spots(self, *args):
        spots = self.trip_controller.current_trip.spots
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
                             self.show_popup('Erro viagem encerrada','Não é possível remover um spot de uma viagem encerrada')
                             if self.trip_controller.finished_trip_check()
                             else self.on_delete_spot_option(spot_object))
            actions_layout.add_widget(view_spot)
            actions_layout.add_widget(update_spot)
            actions_layout.add_widget(delete_spot)

        scrollview.add_widget(table_layout)
        list_spot_layout.add_widget(scrollview)

        # Botao
        buttons_layout = BoxLayout(size_hint=(1, 0.1), padding=10)

        create_spot_button = Button(text="Novo spot", font_size='18sp')
        create_spot_button.bind(on_press=lambda _: self.show_popup('Erro viagem encerrada','Não é possível criar um spot de uma viagem encerrada')
                                if self.trip_controller.finished_trip_check()
                                else self.on_create_spot_option())
        buttons_layout.add_widget(create_spot_button)

        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_return_trip)
        buttons_layout.add_widget(return_button)

        list_spot_layout.add_widget(buttons_layout)

        self.add_widget(list_spot_layout)


    def on_return_trip(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "trip_list"

    def on_create_spot_option(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "spot_create"

    def on_view_spot_option(self, spot):
        self.clear_widgets()
        view_spot_layout = BoxLayout(orientation='vertical')

        # Título
        header_label = Label(text=(spot.name + '   ' + spot.start_hour.split(":")[0][8:10]+'/'+ spot.start_hour.split(":")[0][5:7]+'/'+spot.start_hour.split(":")[0][0:4]), text_size=self.size, font_size='30sp', halign='left', valign='middle')
        view_spot_layout.add_widget(header_label)

        name_box_layout = BoxLayout(orientation='vertical')
        # Nome do spot label
        name_label = Label(text="Nome do spot", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        name_box_layout.add_widget(name_label)

        # Nome do spot
        name = Label(text=(spot.name), text_size=self.size, font_size='18sp', halign='left', valign='middle')
        name_box_layout.add_widget(name)
        view_spot_layout.add_widget(name_box_layout)

        #dentro desse boxlayout horizontal eu tenho 3 boxlayout verticais
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
        start_hour = Label(text=str(spot.start_hour.split(":")[0][-2:]+':'+spot.start_hour.split(":")[1]), text_size=self.size,
                           size=(100, dp(40)),
                           font_size='18sp', halign='center', valign='middle')
        start_hour_vertical_box_layout.add_widget(start_hour_label)
        start_hour_vertical_box_layout.add_widget(start_hour)

        end_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        end_hour_label = Label(text="Hora de fim", text_size=self.size,
                               size=(100, dp(40)), bold=True,
                               font_size='16sp', halign='center', valign='middle')
        end_hour = Label(text=str(spot.end_hour.split(":")[0][-2:]+':'+spot.end_hour.split(":")[1]), text_size=self.size,
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
        categoria_label = Label(text="Rating", text_size=self.size, bold=True, font_size='16sp', halign='left', valign='middle')
        categoria_box_layout.add_widget(categoria_label)

        #categoria
        categoria = Label(text=spot.category.name, text_size=self.size, font_size='18sp', halign='left', valign='middle')
        categoria_box_layout.add_widget(categoria)
        view_spot_layout.add_widget(categoria_box_layout)

        # rating_label
        rating_box_layout = BoxLayout(orientation='vertical')
        rating_label = Label(text="Avaliação", text_size=self.size, bold=True, font_size='16sp',
                                halign='left', valign='middle')
        rating_box_layout.add_widget(rating_label)

        # categoria
        rating = Label(text=str(spot.rating), text_size=self.size, font_size='18sp', halign='left',
                          valign='middle')
        rating_box_layout.add_widget(rating)
        view_spot_layout.add_widget(rating_box_layout)

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
        comment_button = Button(text="Ver comentários", font_size='18sp')
        comment_button.bind(on_press=lambda _, x=spot: self.on_comments(spot))
        button_box_layout.add_widget(return_button)
        button_box_layout.add_widget(comment_button)

        view_spot_layout.add_widget(button_box_layout)

        self.add_widget(view_spot_layout)

    def on_update_spot_option(self, spot):
        self.clear_widgets()
        update_spot_layout = BoxLayout(orientation='vertical')

        #Título
        header_label = Label(text="Edição de spot", text_size=[800,600], font_size='30sp', halign='left', valign='middle')
        update_spot_layout.add_widget(header_label)

        #Nome
        name_box_layout = BoxLayout(orientation='vertical')
        name_label = Label(text="Nome do spot *", text_size=[800,600], font_size='16sp', halign='left', valign='middle')
        name_box_layout.add_widget(name_label)

        #truque para deixar input box menor
        spot_name_input_box = BoxLayout(orientation='vertical')
        spot_name_input = TextInput(text=spot.name,multiline=False)
        spot_name_input_box.add_widget(spot_name_input)
        spot_name_input_box.add_widget(Label())

        name_box_layout.add_widget(spot_name_input_box)

        update_spot_layout.add_widget(name_box_layout)

        #Data e Hora
        horizontal_box_layout = BoxLayout()
        horizontal_box_layout.cols = 4

        start_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        start_hour_label = Label(text="Hora de início *", font_size='16sp',
                                 halign='center', valign='middle')

        start_hour_input = TextInput(text=str(spot.start_hour.split(":")[0][-2:]+':'+spot.start_hour.split(":")[1]), multiline=False)

        start_hour_vertical_box_layout.add_widget(start_hour_label)
        start_hour_vertical_box_layout.add_widget(start_hour_input)

        end_hour_vertical_box_layout = BoxLayout(orientation='vertical')
        end_hour_label = Label(text="Hora de fim *", font_size='16sp',
                                 halign='center', valign='middle')

        end_hour_input = TextInput(text=str(spot.end_hour.split(":")[0][-2:]+':'+spot.end_hour.split(":")[1]), multiline=False)

        ###
        start_date_vertical_box_layout = BoxLayout(orientation='vertical')
        start_date_label = Label(text="Data *", font_size='16sp',
                                 halign='center', valign='middle')

        start_date_input = TextInput(text=str(spot.start_hour.split(":")[0][8:10]+'/'+ spot.start_hour.split(":")[0][5:7]+'/'+spot.start_hour.split(":")[0][0:4]), multiline=False)

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

        update_spot_layout.add_widget(horizontal_box_layout)

        #categoria_valor
        cv_horizontal_box_layout = BoxLayout()
        cv_horizontal_box_layout.cols = 4

        category_vertical_box_layout = BoxLayout(orientation='vertical')
        category_label = Label(text="Categoria *", font_size='16sp',
                                 halign='center', valign='middle')

        category_list = Category.list_by_traveller(self.my_app_instance.traveller_id)

        dropdown_list = DropDown()
        choosen_category = [spot.category]
        for i in category_list:
            category_name = i.name
            text_string = category_name

            btn = Button(text=text_string, size_hint_y=None, height=50)
            btn.bind(on_press=lambda btn, current_category=i:
                     [dropdown_list.select(btn.text),
                      choosen_category.pop(),
                      choosen_category.insert(0, current_category)])

            dropdown_list.add_widget(btn)

        dropdown_list_button = Button()
        dropdown_list_button.bind(on_release=dropdown_list.open)

        dropdown_list.bind(on_select=lambda instance, x:
                           setattr(dropdown_list_button, 'text', x))

        #deixando o valor corrente
        dropdown_list.select(spot.category.name)

        category_vertical_box_layout.add_widget(category_label)
        category_vertical_box_layout.add_widget(dropdown_list_button)

        money_spent_vertical_box_layout = BoxLayout(orientation='vertical')
        money_spent_label = Label(text="Valor", font_size='16sp',
                                 halign='center', valign='middle')
        money_spent_input = TextInput(text=str(spot.money_spent), multiline=False)

        money_spent_vertical_box_layout.add_widget(money_spent_label)
        money_spent_vertical_box_layout.add_widget(money_spent_input)

        #rating
        rating_box_layout = BoxLayout(orientation='vertical')
        rating_label = Label(text="Avaliação", font_size='16sp',
                                  halign='center', valign='middle')
        rating_input = TextInput(text=str(spot.rating), multiline=False)

        rating_box_layout.add_widget(rating_label)
        rating_box_layout.add_widget(rating_input)

        cv_horizontal_box_layout.add_widget(category_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(money_spent_vertical_box_layout)
        cv_horizontal_box_layout.add_widget(rating_box_layout)
        cv_horizontal_box_layout.add_widget(Label())
        cv_horizontal_box_layout.add_widget(Label())

        update_spot_layout.add_widget(cv_horizontal_box_layout)

        members_placeholder_box_layout = BoxLayout()

        members_vertical_box = BoxLayout(orientation='vertical')
        members_label = Label(text="Membros", font_size='16sp',
                                 halign='center', valign='middle')

        members_check_box_placeholder = ScrollView()

        table_layout = GridLayout(cols=1, row_default_height=30, size_hint_y=None, padding=(30, 50, 30, 50))
        table_layout.bind(minimum_height=table_layout.setter('height'))

        members_list = Member.list_by_traveller(self.my_app_instance.traveller_id)

        #posicionando os membros já selecionados
        members_list_output = []
        for member in spot.members:
            members_list_output.append(member)

        for member in members_list:
            line = BoxLayout()
            checkbox = CheckBox()

            #marcando os membros já selecionados
            if member.id in [j.id for j in members_list_output]:
                checkbox.active = True

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

        members_placeholder_box_layout.add_widget(members_vertical_box)
        members_placeholder_box_layout.add_widget(Label())

        update_spot_layout.add_widget(members_placeholder_box_layout)

        bottom_horizontal_box_layout = BoxLayout()
        bottom_horizontal_box_layout.cols = 4

        #status
        status_vertical_box_layout = BoxLayout(orientation='vertical')
        status_label = Label(text="Status *", font_size='16sp',
                                 halign='center', valign='middle')

        status_dropdown_list = DropDown()
        choosen_status = [spot.status]
        options = ['Aberto','Encerrado','Cancelado']
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=50)
            btn.bind(on_press=lambda btn, current_spot=option:
                     [status_dropdown_list.select(btn.text),
                      choosen_status.pop(),
                      choosen_status.insert(0, current_spot)])

            status_dropdown_list.add_widget(btn)

        status_dropdown_list_button = Button()
        status_dropdown_list_button.bind(on_release=status_dropdown_list.open)

        status_dropdown_list.bind(on_select=lambda instance, x:
                           setattr(status_dropdown_list_button, 'text', x))

        status_dropdown_list.select(spot.status)
        status_vertical_box_layout.add_widget(status_label)
        status_vertical_box_layout.add_widget(status_dropdown_list_button)

        save_button_box_layout = BoxLayout(orientation='vertical')
        save_button = Button(text='Salvar', font_size='18sp')
        save_button.bind(on_press=lambda _, x=[spot_name_input,
                                               start_hour_input,
                                               end_hour_input,
                                               choosen_category,
                                               money_spent_input,
                                               members_list_output,
                                               choosen_status,
                                               spot,
                                               start_date_input,
                                               rating_input]:
                         [self.on_save_option(x), print('member_list eh ',
                                                        members_list_output),
                          self.on_update_spot_option])

        save_button_box_layout.add_widget(Label())
        save_button_box_layout.add_widget(save_button)

        return_button_box_layout = BoxLayout(orientation='vertical')
        return_button = Button(text="Voltar", font_size='18sp')
        return_button.bind(on_press=self.on_list_spots)

        return_button_box_layout.add_widget(Label())
        return_button_box_layout.add_widget(return_button)

        bottom_horizontal_box_layout.add_widget(status_vertical_box_layout)
        bottom_horizontal_box_layout.add_widget(Label())
        bottom_horizontal_box_layout.add_widget(save_button_box_layout)
        bottom_horizontal_box_layout.add_widget(return_button_box_layout)

        update_spot_layout.add_widget(bottom_horizontal_box_layout)

        self.add_widget(update_spot_layout)

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

    def on_delete_spot_option(self, spot):
        delete_popup_answer = self.delete_popup(spot)

    def on_save_option(self, arguments_list):
        #string não pode ser vazia
        name_field = self.check_name_field(arguments_list[0].text)
        if name_field is None:
            self.show_popup('Erro Nome','Campo nome não preenchido')
            return

        spot_rating = self.check_name_field(arguments_list[9].text)
        try:
            if not 0 <= int(spot_rating) <= 5:
                self.show_popup('Erro na avaliação', 'A avaliação deve ser um numero entre 0 a 5')
                return
        except Exception as e:
            print(e)
            self.show_popup('Erro na avaliação', 'Ocorreu algum erro inesperado, a avaliação deve ser um numero entre 0 a 5')
            return

        # testes de campo de data de início
        start_hour_datetime = self.check_time_field(arguments_list[1].text)
        if start_hour_datetime is None:
            self.show_popup('Erro hora de início',
                            'A hora deve estar no formato \"HH:MM\"')
            # 'A data e hora deve estar no formato \"AAAA-MM-DD HH:MM:SS\"')
            return
        else:
            start_hour_datetime = start_hour_datetime + ':00'

        # testes de campo de data de fim
        end_hour_datetime = self.check_time_field(arguments_list[2].text)
        if end_hour_datetime is None:
            self.show_popup('Erro hora de fim',
                            'A hora deve estar no formato \"HH:MM\"')
            return
        else:
            end_hour_datetime = end_hour_datetime + ':00'

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

        # testes de campo de data
        start_date = arguments_list[8].text
        if (len(start_date) != 10) or (
                len(start_date.split('/')[2]) != 4 or len(start_date.split('/')[1]) != 2 or len(
                start_date.split('/')[0]) != 2):
            self.show_popup('Erro data',
                            'A data deve estar no formato \"DD/MM/AAAA\"')
            return
        else:
            start_date = f'{(start_date.split("/")[2])}-{(start_date.split("/")[1])}-{(start_date.split("/")[0])}'

        #checar valor dinheiro
        money_float = self.check_money_spent_field(arguments_list[4].text)
        if money_float is None:
            self.show_popup('Erro Dinheiro gasto',
                            'O campo de dinheiro deve estar no formato \"XX,XX\"')
            return

        #checar membros é no controller
        spot_members_list = arguments_list[5]
        status = arguments_list[6][0]
        spot = arguments_list[7]
        update_spot_validation, message = self.trip_controller.update_spot(name_field,
                                                                           money_float,
                                                                           (start_date + ' ' + start_hour_datetime),
                                                                           (start_date + ' ' + end_hour_datetime),
                                                                           category_object,
                                                                           spot_members_list,
                                                                           status,
                                                                           spot,
                                                                           self.my_app_instance.traveller_id,
                                                                           spot_rating)
        if not(update_spot_validation):
            self.show_popup('Erro', message)
        else:
            self.show_popup('Spot atualizado', message)

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
            if (len(time_field) != 5) or (len(time_field.split(':')[0]) != 2 or len(time_field.split(':')[1]) != 2):
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

    def delete_popup(self, spot):
        popup = Popup(title='Confirmar deleção', size_hint=(None, None), size=(500, 200))
        layout = GridLayout(cols=1, spacing=10, padding=10)
        layout.add_widget(Label(text='Você tem certeza que deseja excluir o spot?'))

        return_btn = Button(text='Cancelar', size_hint=(1, None), height=50)
        return_btn.bind(on_press=popup.dismiss)

        confirm_button = Button(text='Confirmar', size_hint=(1, None), height=50)
        confirm_button.bind(on_press=lambda _:
                            [self.trip_controller.delete_spot(spot, popup),
                             self.show_popup('Spot deletado', 'Spot deletado com sucesso'),
                             self.on_list_spots()])

        layout.add_widget(return_btn)
        layout.add_widget(confirm_button)
        popup.add_widget(layout)
        popup.open()

    def on_comments(self, spot, *args):
        self.trip_controller.current_spot = spot
        self.manager.current = 'comment_list'
