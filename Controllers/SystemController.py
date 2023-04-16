from MemberController import MemberController
from UserController import UserController

class SystemController:
    def __init__(self):
        self.__MemberController = MemberController()
        self.__UserController = UserController()

        self.__SystemView = SystemView()
        self.main_loop()

    def main_loop(self):
        while True:
          control_flow_value = self.SystemView.open()

          if control_flow_value == 0:
            break
          elif control_flow_value == 1:
            self.__UserController.login()
            #insira if statement para chamar outra função da classe sistema relacionada a tela principal do sistema
          elif control_flow_value == 2:
            self.__UserController.signin()
