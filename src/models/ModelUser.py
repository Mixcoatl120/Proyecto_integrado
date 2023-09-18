from .entities.Users import User
import psycopg2

db_config = {
    'dbname': 'users',
    'user': 'postgres',
    'password': 'Asea2023',
    'host': 'localhost',
    'port': '5432'
}

class ModelUser():
   @classmethod
   def login(self,db ,user):
       try:
            db = psycopg2.connect(**db_config)
            sql = "SELECT id, username, password, fullname FROM usuarios WHERE username = '{}'".format(user.username)
            cursor = db.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
       except Exception as ex:
           print(ex)

   @classmethod
   def get_by_id(self,db,id):
       try:
           db = psycopg2.connect(**db_config)
           sql = "SELECT id, username, fullname FROM usuarios WHERE id = '{}'".format(id)
           cursor = db.cursor()
           cursor.execute(sql)
           row = cursor.fetchone()
           if row != None:
               logged_user = User(row[0],row[1],None, row[2])
               return logged_user
           else:
               return None
       except Exception as ex:
           print(ex)