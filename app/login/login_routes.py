from flask import Blueprint,Flask,request,redirect,render_template,flash,url_for
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from .models.ModelUser import ModelUser
from .models.entities.Users import User

db = SQLAlchemy()

login = Blueprint('login',__name__,template_folder = 'templates')

@login.route('/login',methods=['POST','GET'])
def Login():
        if request.method == 'POST':
            us = request.form['username']
            user = User(0,request.form['username'],request.form['password'])
            logged_user = ModelUser.login(db,user)
            if logged_user != None:
                if logged_user.pswd:
                    login_user(logged_user)
                    if us == "admin":
                        print("admin")
                        return redirect(url_for('home.Home'))
                    else:
                        print("Usario")
                        return redirect(url_for('home_u.Home_u'))
                else:
                    flash("Contrasena incorrecta")
                    return render_template('login.html')
            else:
                flash('usuario no encontrado')
                return render_template('login.html')
        else:
            return render_template('login.html')
        
@login.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('login.Login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return render_template('errors/404.html')
        return f(*args, **kwargs)
    return decorated_function