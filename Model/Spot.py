from datetime import date
from Model.Category import Category

class Spot:
    def __init__(self, name: str, money_spent: float, start_hour: date,
                 end_hour: date, category: Category, members: list,
                 spot_database_id=None, status='Aberto', rating=None,):
        #database_id será necessário ao buscar os comentários específicos
        #o método de criar um novo spot deve criar o id, e o get_spotsjá tera ele pela busca
        self.__name = name
        self.__money_spent = money_spent
        self.__start_hour = start_hour
        self.__end_hour = end_hour
        self.__category = category
        self.__members = members
        self.__spot_database_id = spot_database_id
        self.__status = status
        self.__rating = rating
        #TODO comentarios serão preenchidos após a instanciacao por alguma funcao da UC de comment
        self.__comments = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @property
    def money_spent(self):
        return self.__money_spent

    @money_spent.setter
    def money_spent(self, new_money_spent: float):
        self.__money_spent = new_money_spent

    @property
    def start_hour(self):
        return self.__start_hour

    @start_hour.setter
    def start_hour(self, new_start_hour: date):
        self.__start_hour = new_start_hour

    @property
    def end_hour(self):
        return self.__end_hour

    @end_hour.setter
    def end_hour(self, new_end_hour: date):
        self.__end_hour = new_end_hour

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status: str):
        self.__status = new_status

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, new_rating: int):
        self.__rating = new_rating

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, new_category: Category):
        self.__category = new_category

    @property
    def members(self):
        return self.__members

    @members.setter
    def members(self, new_members: list):
        self.__members = new_members

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, new_comments: list):
        self.__comments = new_comments

    @property
    def spot_database_id(self):
        return self.__spot_database_id

    @spot_database_id.setter
    def spot_database_id(self, new_spot_database_id):
        self.__spot_database_id = new_spot_database_id
