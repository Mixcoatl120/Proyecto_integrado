from flask import Blueprint,Flask,render_template
from flask_login import login_required
from login.login_routes import admin_required
from dbModel import *
from sqlalchemy import func # importa funciones como la de count
import datetime

home = Blueprint('home',__name__,template_folder = 'templates')

@home.route('/home')
@login_required
@admin_required
def Home():
    fechahoy = datetime.date.today()

    # Materias
    c = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy).scalar()
    A = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '1').scalar()
    CUS = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '2').scalar()
    IA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '3').scalar()
    LBA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '4').scalar()
    RA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '5').scalar()
    T = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '6').scalar()
    # Tramite
    TRA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '1').scalar()
    ASU = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '2').scalar()
    return render_template('home.html',A=A,CUS=CUS,IA=IA,LBA=LBA,RA=RA,T=T,c=c,TRA=TRA,ASU=ASU)