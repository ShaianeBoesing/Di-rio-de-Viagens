import sqlite3
from Database.Database import Database
from Model.Spot import Spot
from Model.Category import Category
from Model.Member import Member
from datetime import date
from Model.Trip import Trip

class TripController:
    def __init__(self):
        self.__trips = {}  # Lista de viagens

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

    def edit_trip(self, title, attributes_to_change: dict):
        self.__update_trip_list()
        if title in self.__trips.keys():
            trip = self.__trips[title]

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

            Database().update('trips', attributes_to_change, 1, ['title', title])
            return True, 'Viagem alterada com sucesso!'
        else:
            return False, 'Viagem nao encontrada!'

    def delete_trip(self, title):
        self.__update_trip_list()
        if title in self.__trips.keys():
            del self.__trips[title]
            Database().delete('trips', 1, ['title', title])

    def __update_trip_list(self, traveller_id):
        table = Database().select(f'SELECT * FROM TRIPS WHERE traveller_id = {traveller_id}')
        print(table)
        self.__trips = {}
        if table is not None:
            for tpl_trip in table:
                title = tpl_trip[1]
                start_date_instance = date(int(tpl_trip[2][0:4]), int(tpl_trip[2][5:7]), int(tpl_trip[2][8:10]))
                end_date_instance = date(int(tpl_trip[3][0:4]), int(tpl_trip[3][5:7]), int(tpl_trip[3][8:10]))
                status = tpl_trip[4]
                trip = Trip(title, start_date_instance, end_date_instance, status)
                self.__trips[tpl_trip[1]] = trip

    #TODO na integração essa função provavelmente será usado pra preencher os
    #spots da trip
    def get_spots(self):
        #select no DB
        database = Database()
        #TODO alterar na integração pra pegar os relativos a viagem
        registers = database.select("SELECT * FROM spots")
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
                                     spot_tuple[4],
                                     spot_tuple[6],
                                     current_spot_id) #faltou comentarios, mas eh outro UC
                spots.append(spot_instance)
            return spots

