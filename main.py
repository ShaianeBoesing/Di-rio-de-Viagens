# from Views.MyApp import MyApp
import datetime
# if __name__ == __main__:
#     MyApp().run()

from Controllers.TripController import TripController
a = TripController()
# print(a.get_trip('teste'))
# # print(a.edit_trip('teste', {'title': 'teste', 'start_date': datetime.date(2023, 6, 11), 'end_date': datetime.date(2023, 6, 28), 'status': 'Terminada'}))
# print(a.get_trip('teste'))
# a.delete_trip('teste')
# print(a.get_trip('teste'))
print(a.create_trip('testea', ['Moc'], [2023, 12, 24], [2023, 12, 29]))
print(a.get_trip('testea'))
print(a.edit_trip('testea', {'title': 'testea', 'start_date': datetime.date(2023, 5, 11), 'end_date': datetime.date(2023, 5, 28), 'status': 'Terminada'}))

