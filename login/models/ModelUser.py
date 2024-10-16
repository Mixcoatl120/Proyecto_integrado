# es el modelo para usuarios, nos permite la verificaicion de la contreseña y la identificacion de id
# para la persistencia del login mediante el id
from .entities.Users import *
from dbModel import *

# search user / buscar usuario
class ModelUser():
    @classmethod
    def login(self,db,user):
        try:
            row = Users.query.filter(Users.login == user.login).first()# query
            if row != None:
                user = User(row.id, row.login, row.pswd, row.name) # user
                return user
            else:
                return None
        except Exception as ex:
            print(ex)

    # id identifier / identificador de id
    @classmethod
    def get_by_id(self,db,id):
        try:
            row = Users.query.filter(Users.id == id).first()# query
            if row != None:
                logged_user = User(row.id, row.login , None, row.name)# user
                return logged_user
            else:
                return None
        except Exception as ex:
            print(ex)
   