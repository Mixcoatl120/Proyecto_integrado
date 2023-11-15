from flask import Flask
from flask_login import LoginManager
from login.models.ModelUser import *
from login.login_routes import *
from admin.home.home_routes import *
from admin.ingreso.ingreso_routes import *
from admin.ingreso_m.ingresom_routes import *
from admin.turnado.turnado_routes import *
from admin.consultas.consultas_routes import *
from admin.cedula.cedula_routes import *
from users.home.home_routes import *
from users.ingreso.ingreso_routes import *
from users.turnado.turnado_routes import *
from users.consultas.consultas_routes import *
from users.cedula.cedula_routes import *
from dbModel import * # modelo de base de datos


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jvm2OrrMd4QaRNHzvtgqfxyLir8' # llave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/siset'# conexion a la base    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
login_manager_app = LoginManager(app) # Configuracion de login
login_manager_app.login_view = "login.Login" #
    
db.init_app(app)

# Funcion para mantener la sesion del usuario activo
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)
    
@app.route('/')
def index():
    return redirect(url_for('login.Login'))

# blueprint de login
app.register_blueprint(login)

#registro de blueprints para administrador
app.register_blueprint(home)
app.register_blueprint(ingreso)
app.register_blueprint(ingresom)
app.register_blueprint(turnado)
app.register_blueprint(consulta)
app.register_blueprint(cedula)

#registro de blueprints para usuarios
app.register_blueprint(home_u)
app.register_blueprint(ingreso_u)
app.register_blueprint(turnado_u)
app.register_blueprint(consulta_u)
app.register_blueprint(cedula_u)

@app.errorhandler(404) # Error 404 por si no encuentra la pagina
def page_not_found(e):
    return render_template('errors/404.html')

def status_401(error): # Error 401 en caso de no iniciar sesion 
    return redirect(url_for('login.Login'))
      
app.register_error_handler(401,status_401)


if __name__ == '__main__':
    app.run()
