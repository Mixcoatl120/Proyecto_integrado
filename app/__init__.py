from flask import Flask
from flask_login import LoginManager
from .login.models import ModelUser
from .login.login_routes import *
from .home.home_routes import *
from .ingreso.ingreso_routes import *
from .turnado.turnado_routes import *
from .consultas.consultas_routes import *
from .cedula.cedula_routes import *
from app.dbModel import * # modelo de base de datos


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Jvm2OrrMd4QaRNHzvtgqfxyLir8' # llave secreta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/siset'# conexion a la base    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    login_manager_app = LoginManager(app) # Configuracion de login
    login_manager_app.login_view = "login.login" #
    
    db.init_app(app)

    # Funcion para mantener la sesion del usuario activo
    @login_manager_app.user_loader
    def load_user(id):
        return ModelUser.get_by_id(db,id)
    
    @app.route('/')
    def index():
        return redirect(url_for('login.Login'))
    
    #registro de blueprints
    app.register_blueprint(login)
    app.register_blueprint(home)
    app.register_blueprint(ingreso)
    app.register_blueprint(turnado)
    app.register_blueprint(consulta)
    app.register_blueprint(cedula)

    @app.errorhandler(404) # Error 404 por si no encuentra la pagina
    def page_not_found(e):
        return render_template('errors/404.html')

    def status_401(error): # Error 401 en caso de no iniciar sesion 
        return redirect(url_for('login'))
    
    app.register_error_handler(401,status_401)

    return app
