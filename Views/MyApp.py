from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from Controllers.MemberController import MemberController
from Controllers.UserController import UserController
from Controllers.CategoryController import CategoryController
from Controllers.TripController import TripController
from Controllers.CommentController import CommentController

from Views.Main.MainView import MainView
from Views.Register.RegisterView import RegisterView
from Views.Login.LoginView import LoginView
from Views.Member.MemberList import MemberList
from Views.Member.MemberCreate import MemberCreate
from Views.Member.MemberEdit import MemberEdit
from Views.Category.CategoryCreate import CategoryCreate
from Views.Category.CategoryEdit import CategoryEdit
from Views.Category.CategoryList import CategoryList
from Views.Spots.SpotView import SpotView
from Views.Spots.SpotCreate import SpotCreate
from Views.Trip.TripList import TripList
from Views.Trip.TripCreate import TripCreate
from Views.Trip.TripEdit import TripEdit
from Views.Comment.CommentList import CommentList
from Views.Comment.CommentCreate import CommentCreate
from Views.Comment.CommentEdit import CommentEdit

class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(MyApp, self).__init__(**kwargs)
		self.__user_controller = UserController()

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.__user_controller = UserController()
        self.__member_controller = MemberController()
        self.__trip_controller = TripController()
        self.__category_controller = CategoryController(self.__trip_controller)
        self.__comment_controller = CommentController(self.__trip_controller)

        self.traveller_id = None


		# Perform any necessary setup tasks here
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainView(name='main_view'))

        sm.add_widget(RegisterView(self.__user_controller, name='register_view'))
        sm.add_widget(LoginView(self.__user_controller, self, name='login_view'))

        sm.add_widget(MemberList(self.__member_controller, self, name='member_list'))
        sm.add_widget(MemberCreate(self.__member_controller, self, name='member_create'))
        sm.add_widget(MemberEdit(self.__member_controller, self, name='member_edit'))

        sm.add_widget(CategoryList(self.__category_controller, self, name='category_list'))
        sm.add_widget(CategoryCreate(self.__category_controller, self, name='category_create'))
        sm.add_widget(CategoryEdit(self.__category_controller, self, name='category_edit'))

        sm.add_widget(SpotView(self.__trip_controller, self, name='spot_view'))
        sm.add_widget(SpotCreate(self.__trip_controller, self, name='spot_create'))

        sm.add_widget(TripList(self.__trip_controller, self, name='trip_list'))
        sm.add_widget(TripCreate(self.__trip_controller, self, name='trip_create'))
        sm.add_widget(TripEdit(self.__trip_controller, self, name='trip_edit'))

        sm.add_widget(CommentList(self.__comment_controller, self, name='comment_list'))
        sm.add_widget(CommentCreate(self.__comment_controller, self, name='comment_create'))
        sm.add_widget(CommentEdit(self.__comment_controller, self, name='comment_edit'))
        return sm

