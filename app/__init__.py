from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .login.models import ModelUser
from .login.login_routes import *
from .home.home_routes import *
from .ingreso.ingreso_routes import *


login_manager = LoginManager()
db = SQLAlchemy()


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
    
    return app