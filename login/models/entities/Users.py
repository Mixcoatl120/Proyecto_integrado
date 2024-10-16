from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin): # contiene los requisitos de inicio de sesion
    def __init__(self, id, login, pswd, name="", active="")-> None:
        self.id = id
        self.login = login
        self.pswd = pswd
        self.name = name
        self.active = active
     
    def is_admin(self):
