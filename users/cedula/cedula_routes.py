from flask import Blueprint,Flask,render_template
from flask_login import login_required
from dbModel import *

cedula_u = Blueprint('cedula_u',__name__,template_folder = 'templates')

@cedula_u.route('/cedula_u')
@login_required
def Cedula():
    return render_template('cedula_u.html')