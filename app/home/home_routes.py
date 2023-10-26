from flask import Blueprint,Flask,request,redirect,render_template,flash,url_for
from flask_login import login_required

home = Blueprint('home',__name__,template_folder = 'templates')

@home.route('/home')
@login_required
def Home():
    return render_template('home.html')