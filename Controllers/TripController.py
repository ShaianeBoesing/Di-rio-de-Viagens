import sqlite3
from Database.Database import Database
from Model.Spot import Spot
from Model.Category import Category
from Model.Member import Member
from datetime import date, datetime
from Model.Trip import Trip

class TripController:
    def __init__(self):
        self.__trips = {}  # Lista de viagens
        self.__spots = []
        self.__current_trip = None
        self.__current_spot = None

    def create_trip(self, title, start_date: date, end_date: date, traveller_id, status: str = 'Em planejamento'):
        self.__update_trip_list(traveller_id)

        # start_date = date(start_date[0], start_date[1], start_date[2])
        # end_date = date(end_date[0], end_date[1], end_date[2])

        if end_date < start_date:
            return False, 'Viagem não criada,data de termino antes da data de começo da viagem'
        for trip in self.__trips.values():
            if trip.title == title:
                return False, 'Viagem não criada por existir outra viagem com mesmo nome!'
            if (trip.start_date <= start_date <= trip.end_date or trip.start_date <= end_date <= trip.end_date) or \
                    (start_date < trip.start_date and end_date>trip.end_date):
                return False, 'Viagem não criada por existir outra viagem datas sobrepostas'

        trip = Trip(title, start_date, end_date, status)
        start_date_month = str(start_date.month) if len(str(start_date.month)) == 2 else'0'+str(start_date.month)
        start_date_day = str(start_date.day) if len(str(start_date.day)) == 2 else'0'+str(start_date.day)
        end_date_month = str(end_date.month) if len(str(end_date.month)) == 2 else '0' + str(end_date.month)
        end_date_day = str(end_date.day) if len(str(end_date.day)) == 2 else '0' + str(end_date.day)
        Database().insert('trips', {'title': title,
                                    'start_date': (str(start_date.year) + '-' +
                                                   start_date_month+'-' + start_date_day),
                                    'end_date': (str(end_date.year)+'-'+end_date_month+'-'+end_date_day),
                                    'status': trip.status, 'traveller_id': traveller_id})
        # traveller_id a ser implementado com a integração do sistema
        self.__trips[title] = trip
        return True, 'Viagem criada com sucesso!'

    def get_trip(self, title):
        if title in self.__trips.keys():
            trip = self.__trips[title]
            return {'title': trip.title, 'start_date': trip.start_date, 'end_date': trip.end_date,
                    'status': trip.status, 'spots': trip.spots[:]}
        else:
            return 'Viagem nao encontrada!'

    def get_trips(self, traveller_id):
        self.__update_trip_list(traveller_id)
        trip_list = []
        for trip in self.__trips.values():
            start_date = str(trip.start_date.day)+'/'+str(trip.start_date.month)+'/'+str(trip.start_date.year)
            end_date = str(trip.end_date.day)+'/'+str(trip.end_date.month)+'/'+str(trip.end_date.year)
            trip_list.append({'title': trip.title, 'start_date': start_date, 'end_date': end_date,
                              'status': trip.status})
        return trip_list

    def edit_trip(self, title, attributes_to_change: dict, traveller_id):
        self.__update_trip_list(traveller_id)
        if title in self.__trips.keys():
            trip = self.__trips[title]
            query = f'SELECT ID FROM TRIPS WHERE title = "{title}" and traveller_id = "{traveller_id}" '
            id = Database().select(query)[0][0]

            if attributes_to_change['title'] != trip.title:
                for loop_trip in self.__trips.values():
                    if loop_trip.title == attributes_to_change['title']:
                        return False, 'Titulo nao alterado, outra viagem encontrada com o mesmo nome'

            if attributes_to_change['start_date'] != trip.start_date:
                for loop_trip in self.__trips.values():
                    if loop_trip.title != trip.title:
                        if trip.end_date < attributes_to_change['start_date']:
                            return False, 'Data não alterada,data de termino antes da data de começo da viagem'
                        if loop_trip.start_date <= attributes_to_change['start_date'] <= loop_trip.end_date or \
                                (attributes_to_change['start_date'] < loop_trip.start_date and
                                 attributes_to_change['end_date'] > loop_trip.end_date):
                            return False, 'Data não alterada por existir outra viagem datas sobrepostas'

            if attributes_to_change['end_date'] != trip.end_date:
                for loop_trip in self.__trips.values():
                    if loop_trip.title != trip.title:
                        if attributes_to_change['end_date'] < trip.start_date == attributes_to_change['start_date']:
                            return False, 'Data não alterada,data de termino antes da data de começo da viagem'
                        elif trip.start_date != attributes_to_change['start_date'] and attributes_to_change['end_date'] != trip.end_date:
                            if attributes_to_change['start_date'] > attributes_to_change['end_date']:
                                return False, 'Data não alterada,data de termino antes da data de começo da viagem'
                        if loop_trip.start_date <= attributes_to_change['end_date'] <= loop_trip.end_date or \
                                (attributes_to_change['start_date'] < loop_trip.start_date and
                                 attributes_to_change['end_date'] > loop_trip.end_date):
                            return False, 'Data não alterada por existir outra viagem datas sobrepostas'

            del self.__trips[trip.title]
            trip.title = attributes_to_change['title']
            self.__trips[attributes_to_change['title']] = trip
            trip.start_date = attributes_to_change['start_date']
            trip.end_date = attributes_to_change['end_date']
            trip.status = attributes_to_change['status']

            Database().update('trips', id,attributes_to_change)
            return True, 'Viagem alterada com sucesso!'
        else:
            return False, 'Viagem nao encontrada!'

    def delete_trip(self, title, traveller_id,):
        self.__update_trip_list(traveller_id)
        if title in self.__trips.keys():
            query = f'SELECT ID FROM TRIPS WHERE title = "{title}" and traveller_id = "{traveller_id}" '
            id = Database().select(query)[0][0]
            Database().delete('trips', id)
            del self.__trips[title]

    def __update_trip_list(self, traveller_id):
        table = Database().select(f'SELECT * FROM TRIPS WHERE traveller_id = {traveller_id}')
        self.__trips = {}
        if table is not None:
            for tpl_trip in table:
                title = tpl_trip[1]
                start_date_instance = date(int(tpl_trip[2][0:4]), int(tpl_trip[2][5:7]), int(tpl_trip[2][8:10]))
                end_date_instance = date(int(tpl_trip[3][0:4]), int(tpl_trip[3][5:7]), int(tpl_trip[3][8:10]))
                status = tpl_trip[4]
                trip = Trip(title, start_date_instance, end_date_instance, status)
                #para já pegar os spots
                trip.spots = self.get_spots(tpl_trip[0])
                self.__trips[tpl_trip[1]] = trip

    def get_trip_id(self, trip_object, traveller_id):
        database = Database()
        trip_list = database.select(f'SELECT * FROM TRIPS WHERE traveller_id = {traveller_id}')
        for trip_tuple in trip_list:
            if trip_tuple[1] == trip_object.title:
                return trip_tuple[0]

    #spots da trip
    def get_spots(self, trip_id):
        #select no DB
        database = Database()
        registers = database.select(f"SELECT * FROM spots WHERE trip_id = {trip_id}")
        if registers is None:
            return []
        else:
            spots = []
            for spot_tuple in registers:
                current_spot_id = spot_tuple[0]
                category = Category.show(spot_tuple[8])

                member_id_list = database.cursor.execute('''SELECT member_id FROM
                                                         spot_members WHERE
                                                         spot_id = ?''',
                                                         (current_spot_id,))
                member_list = []
                for member_id in member_id_list:
                    member_object = Member.show(member_id[0])
                    member_list.append(member_object)

                spot_instance = Spot(spot_tuple[1],
                                     spot_tuple[5],
                                     spot_tuple[2],
                                     spot_tuple[3],
                                     category,
                                     member_list,
                                     current_spot_id,
                                     spot_tuple[4],
                                     spot_tuple[6]) #faltou comentarios, mas eh outro UC
                spots.append(spot_instance)
            return spots

    def create_spot(self,
                    name_field,
                    money_float,
                    start_hour_datetime,
                    end_hour_datetime,
                    category_object,
                    spot_members_list,
                    traveller_id
                    ):

        time_check, member, conflciting_spot_name = self.check_members_spots_time_rule(spot_members_list,
                                                                                  start_hour_datetime,
                                                                                  end_hour_datetime)
        if not(time_check):
            return False, f'''{member.name} já está participando de spot
            {conflciting_spot_name} salvo no mesmo horário'''

        spot_instance = Spot(name_field,
                             money_float,
                             start_hour_datetime,
                             end_hour_datetime,
                             category_object,
                             spot_members_list,
                             )
        #pegando id da trip
        current_trip_id = self.get_trip_id(self.current_trip, traveller_id)
        #salvar registro e pegar database_id
        database = Database()
        values = {"name": spot_instance.name,
                  "start_hour": spot_instance.start_hour,
                  "end_hour": spot_instance.end_hour,
                  "status": spot_instance.status,
                  "value": spot_instance.money_spent,
                  "rating": spot_instance.rating,
                  "trip_id": current_trip_id,
                  "category_id": spot_instance.category.id}
        new_database_id = database.insert("spots", values)

        #coloca o database id correto
        spot_instance.spot_database_id = new_database_id
        #adiciona a instancia ao controlador
        self.spots.append(spot_instance)

        #atulizar tabela relacional spot_members
        self.create_spot_members_table_registers(spot_instance.members,
                                                spot_instance.spot_database_id)

        return True, 'Spot criado com sucesso'

    def update_spot(self,
                    name_field,
                    money_float,
                    start_hour_datetime,
                    end_hour_datetime,
                    category_object,
                    spot_members_list,
                    status,
                    spot,
                    traveller_id,
                    spot_rating):

        time_check, member, conflciting_spot_name = self.check_members_spots_time_rule(spot_members_list,
                                                                                  start_hour_datetime,
                                                                                  end_hour_datetime,
                                                                                       spot)
        if not(time_check):
            return False, f'''{member.name} já está participando de spot
            {conflciting_spot_name} salvo no mesmo horário'''

        #fazendo alterações na intância
        spot.name = name_field
        spot.money_spent = money_float
        spot.start_hour = start_hour_datetime
        spot.end_hour = end_hour_datetime
        spot.category = category_object
        spot.rating = spot_rating
        spot.status = status

        #deletando antigos, inserindo novos
        self.delete_spot_members_table_registers(spot.members, spot.spot_database_id)
        self.create_spot_members_table_registers(spot_members_list, spot.spot_database_id)

        #atualiza a instancia
        spot.members = spot_members_list

        #pegando trip_id
        current_trip_id = self.get_trip_id(self.current_trip, traveller_id)
        #alterando registros no db
        database = Database()
        values = {"name": spot.name,
                  "start_hour": spot.start_hour,
                  "end_hour": spot.end_hour,
                  "status": spot.status,
                  "value": spot.money_spent,
                  "rating": spot.rating,
                  "trip_id": current_trip_id,
                  "category_id": spot.category.id}
        database.update("spots", spot.spot_database_id, values)

        return True, 'Spot editado com sucesso'

    def delete_spot(self, spot, popup):
        popup.dismiss()
        #remover do database
        database = Database()
        database.delete('spots', spot.spot_database_id)

        #remover da lista da trip atual
        self.current_trip.spots.remove(spot)

    def check_members_spots_time_rule(self, spot_members_list, start_time, end_time, current_spot):
        database = Database()
        start_time_parameter = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time_parameter = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        for member in spot_members_list:
            member_spots = database.select(f'SELECT spot_id FROM spot_members WHERE member_id={member.id}')
            for member_spot in member_spots:
                spot_id = member_spot[0]
                #if spot_id ==
                spot_registers = database.select(f'SELECT * FROM spots WHERE id={spot_id}')
                for spot in spot_registers:
                    if spot[0] != current_spot.spot_database_id:
                        print('spot eh', spot)
                        start_hour_datetime_object = datetime.strptime(spot[2], '%Y-%m-%d %H:%M:%S')
                        end_hour_datetime_object = datetime.strptime(spot[3], '%Y-%m-%d %H:%M:%S')
                        if start_hour_datetime_object >= start_time_parameter and start_hour_datetime_object <= end_time_parameter:
                            return False, member, spot[1]
                        if end_hour_datetime_object >= start_time_parameter and end_hour_datetime_object <= end_time_parameter:
                            return False, member, spot[1]
        return True, None, None

    def create_spot_members_table_registers(self, members_list, spot_id):
        #print('members_list eh ', members_list)
        for member in members_list:
            member.save_spot_member(spot_id)

    def delete_spot_members_table_registers(self, members_list, spot_id):
        for member in members_list:
            member.delete_spot_member(spot_id)

    def finished_trip_check(self):
        if self.current_trip.status == 'Encerrado':
            return True
        else:
            False

    def cancel_all_spots(self):
        spot_list = self.current_trip.spots
        for spot in spot_list:
            if spot.status == 'Aberto':
                spot.status = 'Cancelado'

                #mudando no database
                database = Database()
                database.raw_sql(f"UPDATE spots SET status = 'Cancelado' WHERE id = {spot.spot_database_id}")

    @property
    def spots(self):
        return self.__spots

    @spots.setter
    def spots(self, new_spots):
        self.__spots = new_spots

    @property
    def current_trip(self):
        return self.__current_trip

    @current_trip.setter
    def current_trip(self, new_trip):
        self.__current_trip = new_trip

    @property
    def current_spot(self):
        return self.__current_spot

    @current_spot.setter
    def current_spot(self, new_spot):
        self.__current_spot = new_spot

    @property
    def trips(self):
        return self.__trips

    def get_all_trips_from_traveller(self, traveller_id):
        database = Database()
        db_tuples = database.select(f'SELECT * FROM trips WHERE traveller_id = {traveller_id}')
        trips_list = []
        for register in db_tuples:
            trip_instance = Trip(register[1], register[2], register[3], register[4])
            trip_instance.spots = self.get_spots(register[0])
            trips_list.append(trip_instance)

        return trips_list

