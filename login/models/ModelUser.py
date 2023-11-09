# es el modelo para usuarios, nos permite la verificaicion de la contreseña y la identificacion de id
# para la persistencia del login mediante el id
from .entities.Users import *
import psycopg2
from config import db_config

# Clase para la busqueda de usuario
class ModelUser():
   
   @classmethod
   def login(self ,db ,user):
       try:
           db = psycopg2.connect(**db_config) # Conexion de la base de datos
           sql = "SELECT id, login, pswd, name FROM admin_users WHERE login = '{}' and active = 'Y'".format(user.login)
           cursor = db.cursor() # cursor para la busqueda 
           cursor.execute(sql) # ejecuta la sentencia de busqueda
           row = cursor.fetchone() # obtine la fila que coincida con la busqueda
           if row != None: # verifica si el valor de la fila si esta vacia
               user = User(row[0], row[1], row[2], row[3]) # almacena los datos en la variable user, mediante la clase user
               cursor.close()
               db.close()
               return user # retorna la variable user
           else:
                return None # no retorna ningun valor 
       except Exception as ex:
           print(ex) # imprime excepcion

    # clase para el inicio de sesion mediante el id

   @classmethod
   def get_by_id(self, db, id):
       try:
           db = psycopg2.connect(**db_config) # conecion de la base de datos
           sql = "SELECT id, login, pswd, name FROM admin_users WHERE id = '{}' and active = 'Y'".format(id) # sentencia sql
           cursor = db.cursor() # creacion de el cursor
           cursor.execute(sql) # ejecucion de la sentencia sql
           row = cursor.fetchone() # obtencion de la fila resultante
           if row != None:
               logged_user = User(row[0],row[1],None, row[3])# variables para el logueo de usuario
                             # en la tercera variable de la clase user no se necesita ya que se comparo la contraseña anteriormente
               cursor.close()
               db.close() 
               return logged_user # retorna el id de login para mantener la sesion iniciada
           else:
               return None
       except Exception as ex: # bloque de exepciones
           print(ex)# imprecion de exepcion