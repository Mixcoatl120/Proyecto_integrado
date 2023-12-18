﻿from flask import Blueprint,Flask,render_template
from flask_login import login_required
from dbModel import *
from sqlalchemy import func,case # importa funciones como Count
import datetime

home_u = Blueprint('home_u',__name__,template_folder = 'templates')

@home_u.route('/home_u')
@login_required
def Home_u():
    fechahoy = datetime.date.today() # establece la fecha de hoy
    #fechahoy = '2023/03/21'
    # Materias
    g_mat = (
        db.session.query(
            Materia.materia,
            func.count(Seguimiento.materia).label('suma'))
            .select_from(Seguimiento)
            .join(Materia, Materia.id == Seguimiento.materia)
            .filter(Seguimiento.fsolicitud == fechahoy)
            .group_by(Materia.id)
            .order_by(Materia.id)
            .all())

    labels_mat = [row.materia for row in g_mat] # se obtiene los nombres de las materias
    data_mat = [row.suma for row in g_mat]# se obtienen los valores correspondientes de materias
    c = db.session.query(func.count(Seguimiento.fsolicitud)).filter(Seguimiento.fsolicitud == fechahoy).scalar() # se obtiene la suma total de tramites


    # Asuntos
    g_asu = (
        db.session.query(
            Asunto.tipo,
            func.count(Seguimiento.tipo_asunto).label('suma'))
            .select_from(Seguimiento)
            .join(Asunto, Asunto.id == Seguimiento.tipo_asunto)
            .filter(Seguimiento.fsolicitud == fechahoy)
            .group_by(Asunto.id)
            .order_by(Asunto.id)
            .all())
    
    labels_asu = [row.tipo.strip() for row in g_asu] # se obtiene los nombres de las asunto
    data_asu = [row.suma for row in g_asu]# se obtienen los valores correspondientes de asunto

    d = db.session.query(func.count(Seguimiento.tipo_asunto)).filter(Seguimiento.fsolicitud == fechahoy, Seguimiento.tipo_asunto != 0).scalar() # se obtiene la suma total de tramites


    dg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general

    # tabla
    resultados = (
        db.session.query(
            Materia.materia,
            func.count(case((Dir_Gen.id == 1, Materia.materia), else_=None)).label('DGGC'),
            func.count(case((Dir_Gen.id == 2, Materia.materia), else_=None)).label('DGGTA'),
            func.count(case((Dir_Gen.id == 3, Materia.materia), else_=None)).label('DGGEERC'),
            func.count(case((Dir_Gen.id == 4, Materia.materia), else_=None)).label('DGGPI'),
            func.count(case((Dir_Gen.id == 5, Materia.materia), else_=None)).label('DGGEERNCM'),
            func.count(case((Dir_Gen.id == 9, Materia.materia), else_=None)).label('DGGOI'),
            func.count(case((Dir_Gen.id == 10, Materia.materia), else_=None)).label('DGIE'),
            func.count(case((Dir_Gen.id == 11, Materia.materia), else_=None)).label('DGGPITA'),
            )
            .select_from(Seguimiento)
            .join(Materia, Materia.id == Seguimiento.materia)
            .join(Dir_Gen, Dir_Gen.id == Seguimiento.dirgralfirma)
            .filter(Seguimiento.fsolicitud == fechahoy)
            .filter(Dir_Gen.cve_unidad == 2)
            .group_by(Materia.id)
            .order_by(Materia.id)
            .all()
    )
    total = 0
    res = []
    
    for r in resultados:
        suma = 0
        for valor in r:
            if isinstance(valor, (int, float)):  # Verifica si el espacio contine un strig 
                suma += valor
        total += suma # suma total de valores en sumas

        res.append({
            'Materia':r.materia,
            'DGGC':r.DGGC,
            'DGGTA':r.DGGTA,
            'DGGEERC':r.DGGEERC,
            'DGGPI':r.DGGPI,
            'DGGEERNCM':r.DGGEERNCM,
            'DGGOI':r.DGGOI,
            'DGIE':r.DGIE,
            'DGGPITA':r.DGGPITA,
            'Total':suma

        })

    # Cierra la sesión después de usarla
    db.session.close()

   # sumas por columna
    num_columnas = len(resultados[0]) if resultados else 0
    sum_col = [0] * num_columnas
    for r in resultados:
        for i, valor in enumerate(r):
            if isinstance(valor, (int, float)):
                sum_col[i] += valor

    # En caso de no tener ningun valor en sum por columna se rellena con 0
    sum_col = ['Total'] + [val if val > 0 else 0 for val in sum_col[1:]]
    
    sum_col[0] = "Total"  # cambia el primer resultado por Total

    return render_template('home_u.html',
                           c=c, # C REPRESENTA EL TOTAL DE TRAMITES
                           labels_mat=labels_mat,data_mat=data_mat, # variables perteneciantes a materia
                           d=d, # es el total de asuntos
                           labels_asu=labels_asu,data_asu=data_asu,# variables pertenecientes Asuntos 
                           # Consultas
                           dg=dg,resultados=resultados,res=res,
                           total=total,
                           sumas_por_columna=sum_col
                           )