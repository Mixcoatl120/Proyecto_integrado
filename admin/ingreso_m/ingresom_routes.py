from flask import Blueprint,Flask,request,render_template,jsonify
from flask_login import login_required
from login.login_routes import admin_required
from dbModel import *

ingresom = Blueprint('ingresom',__name__,template_folder = 'templates')