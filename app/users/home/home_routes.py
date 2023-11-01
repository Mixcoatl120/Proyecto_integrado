from flask import Blueprint,Flask,render_template
from flask_login import login_required

home_u = Blueprint('home_u',__name__,template_folder = 'templates')

@home_u.route('/home_u')
@login_required
def Home_u():
    return render_template('home_u.html')