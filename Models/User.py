import re


class User:
    def __init__(self, username, name, password):
        self.__username = username
        self.__name = name
        self.__password = password

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if re.search(r'\d', value):
            raise ValueError("O nome não deve conter numeros!")
        self.__name = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value
