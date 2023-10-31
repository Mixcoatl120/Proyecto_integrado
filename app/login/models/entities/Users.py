from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,login, pswd, name="",active="")-> None:
        self.id = id
        self.login = login
        self.pswd = pswd
        self.name = name
        self.active = active

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)