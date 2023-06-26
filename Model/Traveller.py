class Traveller:
    def __init__(self, username: str, name: str, password: str, traveller_id=None):
        self.__username = username
        self.__name = name
        self.__password = password
        self.__traveller_id = traveller_id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    # a senha já chega no model hasheada pelo controller
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def traveller_id(self):
        return self.__traveller_id
