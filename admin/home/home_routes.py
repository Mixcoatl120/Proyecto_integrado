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
    #fechahoy = datetime.date.today()
    fechahoy = '2023/03/22'
    # Materias
    c = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy).scalar()
    A = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '1').scalar()
    CUS = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '2').scalar()
    IA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '3').scalar()
    LBA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '4').scalar()
    RA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '5').scalar()
    T = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '6').scalar()
    RP = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '7').scalar()
    SC = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '8').scalar()
    S = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '9').scalar()
    SAS = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '10').scalar()
    PD = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '11').scalar()
    AA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '12').scalar()
    RME = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '13').scalar()
    PRE = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '15').scalar()
    ES = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '16').scalar()
    M = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '17').scalar()
    CDA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '18').scalar() 
    N = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '19').scalar()
    TPPPMD = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '20').scalar()
    YC = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '21').scalar()
    YNC = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.materia == '22').scalar()
    # Tramite
    TRA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '1').scalar()
    ASU = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '2').scalar()
    return render_template('home.html',c=c,A=A,CUS=CUS,IA=IA,LBA=LBA,RA=RA,T=T,RP=RP,SC=SC,S=S,SAS=SAS,PD=PD,AA=AA,RME=RME,PRE=PRE,
                           ES=ES,M=M,CDA=CDA,N=N,TPPPMD=TPPPMD,YC=YC,YNC=YNC,
                           TRA=TRA,ASU=ASU)