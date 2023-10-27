from flask import Blueprint,Flask,render_template,request
from flask_login import login_required
from app.dbModel import *

cedula = Blueprint('cedula',__name__,template_folder = 'templates')

@cedula.route('/cedula')
@login_required
def Cedula():
    return render_template('cedula.html')