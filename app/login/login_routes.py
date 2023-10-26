from flask import Blueprint,Flask,request,redirect,render_template,flash,url_for
from flask_login import LoginManager,login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from .models.ModelUser import ModelUser
from .models.entities.Users import User

db = SQLAlchemy()

login = Blueprint('login',__name__,template_folder = 'templates')

@login.route('/login',methods=['POST','GET'])
def Login():
        if request.method == 'POST':
            user = User(0,request.form['username'],request.form['password'])
            logged_user = ModelUser.login(db,user)
            if logged_user != None:
                if logged_user.pswd:
                    login_user(logged_user)
                    return redirect(url_for('home.Home'))
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