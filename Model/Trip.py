from datetime import date

class Trip:
    def __init__(self, title: str, start_date: date, end_date: date, status: str):
        self.__title = title
        self.__start_date = start_date
        self.__end_date = end_date
        self.__status = status
        # TODO: self.__spots methods
        self.__spots = []

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date):
        self.__end_date = end_date

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date):
        self.__start_date = start_date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def members(self):
        return self.__members

    @members.setter
    def members(self, members):
        self.__members = members

    @property
    def cities(self):
        return self.__cities

    @cities.setter
    def cities(self, cities):
        self.__cities = cities

    # TODO: Implementar métodos restantes de spots na integração.
    @property
    def spots(self):
        return self.__spots

    @spots.setter
    def spots(self, spots):
        self.__spots = spots