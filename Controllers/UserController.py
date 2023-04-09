import os
import pickle

from Model.User import User


class UserController:
    def __init__(self):
        self.users = []
        self.load_users()

    def register_user(self, username, name, password):
        # Check if the username is already taken
        if any(user.username == username for user in self.users):
            return False

        # Create a new user and add it to the list
        user = User(username, name, password)
        self.users.append(user)
        self.save_users()
        return True

    def save_users(self):
        # Save the users to a file using the pickle package
        with open('users.pickle', 'wb') as f:
            pickle.dump(self.users, f)

    def load_users(self):
        # Load the users from the file if it exists
        if os.path.exists('users.pickle'):
            with open('users.pickle', 'rb') as f:
                self.users = pickle.load(f)
