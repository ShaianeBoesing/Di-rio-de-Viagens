import sqlite3
from Database.Database import Database
from Model.Spot import Spot
from Model.Category import Category
from Model.Member import Member

class TripController:
    def __init__(self):
        pass

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

