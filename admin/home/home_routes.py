from flask import Blueprint,Flask,render_template
from flask_login import login_required
from login.login_routes import admin_required
from dbModel import *
from sqlalchemy import func,case # importa funciones como Count
import datetime

home = Blueprint('home',__name__,template_folder = 'templates')

@home.route('/home')
@login_required
@admin_required
def Home():
    #fechahoy = datetime.date.today()
    fechahoy = '2023/03/30'
    # Materias
    #   |     select    |   count  |          from         |                Where                    |          |
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
    SM = A + CUS + IA + LBA + RA + T + RP + SC + S + SAS + PD + AA + RME + PRE + ES + M + CDA + N + TPPPMD + YC +YNC 
    # Asuntos
    JO = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '1').scalar()
    DP = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '2').scalar()
    CNDH = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '3').scalar()
    OIC = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '4').scalar()
    PGR = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '5').scalar()
    JA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '6').scalar()
    JCA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '7').scalar()
    RR = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '8').scalar()
    CON = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '9').scalar()
    CUM = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '10').scalar()
    I = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '11').scalar()
    PT = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '12').scalar()
    SO = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '13').scalar()
    NOT = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '14').scalar()
    AVI = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '15').scalar()
    CC = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_asunto == '16').scalar()
    SA = JO + DP + CNDH + OIC + PGR + JA + JCA + RR + CON + CUM + I + PT + SO + NOT + AVI + CC 
    # Tramite
    TRA = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '1').scalar()
    ASU = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy,Seguimiento.tipo_ingreso == '2').scalar()
    SI = TRA + ASU
    dg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general

    resultados = db.session.query(
        Materia.materia,
        db.func.count(db.case(([(Dir_Gen.id == 1, Materia.materia)].label('DGGC'),)))
        db.func.count(db.case(([(Dir_Gen.id == 2, Materia.materia)].label('DGGTA'),)))
        db.func.count(db.case(([(Dir_Gen.id == 3, Materia.materia)].label('DGGEERC'),)))
        db.func.count(db.case(([(Dir_Gen.id == 4, Materia.materia)].label('DGGPI'),)))
        db.func.count(db.case(([(Dir_Gen.id == 5, Materia.materia)].label('DGGEERNMC'),)))
        db.func.count(db.case(([(Dir_Gen.id == 9, Materia.materia)].label('DGGOI'),)))
        db.func.count(db.case(([(Dir_Gen.id == 10, Materia.materia)].label('DGGIE'),)))
        db.func.count(db.case(([(Dir_Gen.id == 11, Materia.materia)].label('DGGPITA'))))
    ).join(
        Seguimiento, Seguimiento.materia == Materia.id
    ).join(
        Dir_Gen, Seguimiento.dirgralfirma == Dir_Gen.id
    ).filter(
        Seguimiento.fsolicitud == '2023/03/30',
        Dir_Gen.cve_unidad == 2
    ).group_by(
        Materia.id
    ).order_by(
        Materia.id
    ).all()

    return render_template('home.html',c=c, # C REPRESENTA EL TOTAL DE TRAMITES 
                           # Estas variables son las que pertenecen a materia 
                           A=A,CUS=CUS,IA=IA,LBA=LBA,RA=RA,T=T,RP=RP,SC=SC,S=S,SAS=SAS,PD=PD,AA=AA,RME=RME,PRE=PRE,
                           ES=ES,M=M,CDA=CDA,N=N,TPPPMD=TPPPMD,YC=YC,YNC=YNC,
                           # Estas variables pertenecen a Asuntos 
                           JO=JO,DP=DP,CNDH=CNDH,OIC=OIC,PGR=PGR,JA=JA,JCA=JCA,RR=RR,CON=CON,CUM=CUM,I=I,PT=PT,SO=SO,NOT=NOT,AVI=AVI,CC=CC,
                           # Estas variables pertenecen a tramite
                           TRA=TRA,ASU=ASU,
                           # Estas son las sumas de cada categoria 
                           SM=SM,SA=SA,SI=SI,
                           # Consultas
                           dg=dg,resultados=resultados
                           )