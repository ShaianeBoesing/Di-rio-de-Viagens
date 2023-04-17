class User:
    def __init__(self, username: str, name: str, password: str):
        self.__username = username
        self.__name = name
        self.__password = password

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, new_username: str):
        self.username = new_username

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.name = new_name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password: str):
        self.password = new_password

