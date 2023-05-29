from Model.Trip import Trip
from Database.Database import Database
from datetime import date

class TripController:
    def __init__(self):
        self.__trips = {}  # Lista de viagens
        self.__update_trip_list()

    def create_trip(self, title, cities, start_date: list, end_date: list, status: str = 'Em planejamento'):
        self.__update_trip_list()

        start_date = date(start_date[0], start_date[1], start_date[2])
        end_date = date(end_date[0], end_date[1], end_date[2])

        if end_date < start_date:
            return False, 'Viagem não criada,data de termino antes da data de começo da viagem'
        for trip in self.__trips.values():
            if trip.title == title:
                return False, 'Viagem não criada por existir outra viagem com mesmo nome!'
            if (trip.start_date <= start_date <= trip.end_date or trip.start_date <= end_date <= trip.end_date) or \
                    (start_date < trip.start_date and end_date>trip.end_date):
                return False, 'Viagem não criada por existir outra viagem datas sobrepostas'

        trip = Trip(title, start_date, end_date, status)
        Database().insert('trips', {'title': title,
                                    'start_date': (str(start_date.year) + '-' +
                                                   str(start_date.month)+'-' + str(start_date.day)),
                                    'end_date': (str(end_date.year)+'-'+str(end_date.month)+'-'+str(end_date.day)),
                                    'status': trip.status, 'traveller_id': '1'})
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
        else:
            return False, 'Viagem nao encontrada!'

    def delete_trip(self, title):
        self.__update_trip_list()
        if title in self.__trips.keys():
            del self.__trips[title]
            Database().delete('trips', 1, ['title', title])

    def __update_trip_list(self):
        table = Database().select_all('trips')
        self.__trips = {}
        for tpl_trip in table:
            title = tpl_trip[1]
            start_date_instance = date(int(tpl_trip[2][0:4]), int(tpl_trip[2][5:7]), int(tpl_trip[2][8:10]))
            end_date_instance = date(int(tpl_trip[3][0:4]), int(tpl_trip[3][5:7]), int(tpl_trip[3][8:10]))
            status = tpl_trip[4]
            trip = Trip(title, start_date_instance, end_date_instance, status)
            self.__trips[tpl_trip[1]] = trip
