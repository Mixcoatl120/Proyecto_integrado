from flask import Blueprint,Flask,render_template
from flask_login import login_required

home = Blueprint('home',__name__,template_folder = 'templates')

@home.route('/home')
@login_required
def Home():
    return render_template('home.html')