from flask import Blueprint,Flask,render_template
from flask_login import login_required
from dbModel import *
from sqlalchemy import func,case # importa funciones como Count
import datetime

home_u = Blueprint('home_u',__name__,template_folder = 'templates')

@home_u.route('/home_u')
@login_required
def Home_u():
    #fechahoy = datetime.date.today() # establece la fecha de hoy
    fechahoy = '2023/12/15'
    dg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    # Materias
    g_mat = (
        db.session.query(
            Materia.materia,
            func.count(Seguimiento.materia).label('suma'))
            .select_from(Seguimiento)
            .join(Materia, Materia.id == Seguimiento.materia) 
            .join(Dir_Gen, Dir_Gen.id == Seguimiento.dirgralfirma) 
            .join(Tip_ing,Tip_ing.id == Seguimiento.tipo_ingreso)
            .filter(Seguimiento.fsolicitud == fechahoy) 
            .filter(Tip_ing.id == 1)
            .group_by(Materia.id)
            .order_by(Materia.id)
            .all())

    labels_mat = [row.materia for row in g_mat] # se obtiene los nombres de las materias
    data_mat = [row.suma for row in g_mat]# se obtienen los valores correspondientes de materias

    e = db.session.query(func.count(Seguimiento.tipo_ingreso)).filter(Seguimiento.fsolicitud == fechahoy).scalar() # se obtiene la suma de ingresos del dia
    d = db.session.query(func.count(Seguimiento.tipo_ingreso)).filter(Seguimiento.tipo_ingreso == 1,Seguimiento.fsolicitud == fechahoy).scalar() # se obtiene la suma tramites
    c = db.session.query(func.count(Seguimiento.tipo_ingreso)).filter(Seguimiento.tipo_ingreso == 2,Seguimiento.fsolicitud == fechahoy).scalar() # se obtiene la suma asuntos


    # Asuntos
    g_asu = (
        db.session.query(
            Asunto.tipo,
            func.count(Seguimiento.tipo_asunto).label('suma'))
            .select_from(Seguimiento)
            .join(Asunto, Asunto.id == Seguimiento.tipo_asunto) 
            .join(Dir_Gen, Dir_Gen.id == Seguimiento.dirgralfirma)
            .join(Tip_ing,Tip_ing.id == Seguimiento.tipo_ingreso) 
            .filter(Seguimiento.fsolicitud == fechahoy) 
            .filter(Tip_ing.id == 2)
            .group_by(Asunto.id)
            .order_by(Asunto.id)
            .all())
    
    labels_asu = [row.tipo.strip() for row in g_asu] # se obtiene los nombres de las asunto
    data_asu = [row.suma for row in g_asu]# se obtienen los valores correspondientes de asunto
    # tabla asuntos
    resultados = (
        db.session.query(
            Asunto.tipo,
            func.count(case((Dir_Gen.id == 1, Asunto.tipo), else_=None)).label('DGGC'),
            func.count(case((Dir_Gen.id == 2, Asunto.tipo), else_=None)).label('DGGTA'),
            func.count(case((Dir_Gen.id == 3, Asunto.tipo), else_=None)).label('DGGEERC'),
            func.count(case((Dir_Gen.id == 4, Asunto.tipo), else_=None)).label('DGGPI'),
            func.count(case((Dir_Gen.id == 5, Asunto.tipo), else_=None)).label('DGGEERNCM'),
            func.count(case((Dir_Gen.id == 9, Asunto.tipo), else_=None)).label('DGGOI'),
            func.count(case((Dir_Gen.id == 10, Asunto.tipo), else_=None)).label('DGIE'),
            func.count(case((Dir_Gen.id == 11, Asunto.tipo), else_=None)).label('DGGPITA'),
            )
            .select_from(Seguimiento)
            .join(Asunto,Asunto.id == Seguimiento.tipo_asunto)
            .join(Dir_Gen, Dir_Gen.id == Seguimiento.dirgralfirma) 
            .join(Tip_ing,Tip_ing.id == Seguimiento.tipo_ingreso)
            .filter(Seguimiento.fsolicitud == fechahoy) 
            .filter(Tip_ing.id == 2)
            .group_by(Asunto.id)
            .order_by(Asunto.id)
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
            'Asunto':r.tipo,
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

    # tabla materia
    resultados2 = (
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
            .join(Tip_ing,Tip_ing.id == Seguimiento.tipo_ingreso)
            .filter(Seguimiento.fsolicitud == fechahoy)
            .filter(Tip_ing.id == 1)
            .group_by(Materia.id)
            .order_by(Materia.id)
            .all()
    )
    total2 = 0
    res2 = []
    
    for r2 in resultados2:
        suma2 = 0
        for valor2 in r2:
            if isinstance(valor2, (int, float)):  # Verifica si el espacio contine un strig 
                suma2 += valor2
        total2 += suma2 # suma total de valores en sumas

        res2.append({
            'Materia':r2.materia,
            'DGGC':r2.DGGC,
            'DGGTA':r2.DGGTA,
            'DGGEERC':r2.DGGEERC,
            'DGGPI':r2.DGGPI,
            'DGGEERNCM':r2.DGGEERNCM,
            'DGGOI':r2.DGGOI,
            'DGIE':r2.DGIE,
            'DGGPITA':r2.DGGPITA,
            'Total':suma2

        })
    # Cierra la sesión después de usarla
    db.session.close()

   # -------------------------------------------------------------
   # sumas por columna de asuntos
    num_columnas = len(resultados[0]) if resultados else 0
    sum_col = [0] * num_columnas
    for r in resultados:
        for i, valor in enumerate(r):
            if isinstance(valor, (int, float)):
                sum_col[i] += valor

    # En caso de no tener ningun valor en sum por columna se rellena con 0
    sum_col = ['Total'] + [val if val > 0 else 0 for val in sum_col[1:]]
    
    sum_col[0] = "Total"  # cambia el primer resultado por Total
    # --------------------------------------------------------------------------------------
    # sumas por columna de materia
    num_columnas2 = len(resultados2[0]) if resultados2 else 0
    sum_col2 = [0] * num_columnas2
    for r in resultados2:
        for i, valor2 in enumerate(r):
            if isinstance(valor2, (int, float)):
                sum_col2[i] += valor2

    # En caso de no tener ningun valor en sum por columna se rellena con 0
    sum_col2 = ['Total'] + [val2 if val2 > 0 else 0 for val2 in sum_col2[1:]]
    
    sum_col2[0] = "Total"  # cambia el primer resultado por Total
    return render_template('home_u.html',
                           e=e, # total de ingresos
                           c=c, # C REPRESENTA EL TOTAL DE TRAMITES
                           labels_mat=labels_mat,data_mat=data_mat, # variables perteneciantes a materia
                           d=d, # es el total de asuntos
                           labels_asu=labels_asu,data_asu=data_asu,# variables pertenecientes Asuntos 
                           dg=dg,# etiquetas de direccion general 

                           resultados=resultados,resultados2=resultados2,
                           res=res,res2=res2,# datos pertenecientes a la tabla de asuntos
                           total=total,total2=total2,
                           sum_col=sum_col,sum_col2=sum_col2
                           )