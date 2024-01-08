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
        return self.login == 'admin' # verifica si el perfil es el administrador

    @classmethod # en caso de que las contraseñas esten encryptadas, desencripta y compara la contraseña dada
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)