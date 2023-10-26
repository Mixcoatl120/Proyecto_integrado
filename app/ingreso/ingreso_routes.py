from flask import Blueprint,Flask,request,render_template,jsonify
from flask_login import login_required
from app.dbModel import *

ingreso = Blueprint('ingreso',__name__,template_folder = 'templates')

@ingreso.route('/ingreso/')
@login_required
def Ingresos():
    ti = Tip_ing.query.all() # consulta a tabla de tipo ingreso
    asu = Asunto.query.all() # consulta a tabla de asunto
    mat = Materia.query.all() # consulta a tabla de materia
    des = Descripcion.query.all()# consulta a tabla de descripcion
    pro = Procedencia.query.all()# consulta a tabla de procedencia
    cad_val = Cad_val.query.all()# consulta a cadena de valor
    dirg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    tp = Tip_per.query.all()# Consulta a tabla de tipo persona
    res = Personal.query.filter_by(active = 'Y').all()# Cpnsulta a tabla de personal
    return render_template('inicio/ingreso.html',ti=ti,asu=asu,mat=mat,dirg=dirg,des=des,pro=pro,cad_val=cad_val,tp=tp,res=res)

@ingreso.route('/ingreso/<materia_id>')
@login_required
def Opc(materia_id):
    tramites = Tramite.query.filter_by(cvetramite = materia_id).all()
    tramites = [{'idtram':t.idtram,
                 'cvetramite': t.cvetramite,
                 'cofemer':t.cofemer
                 } for t in tramites]
    return jsonify(tramites)

# predecir responsable
@ingreso.route('/ingreso/auto', methods=['GET'])
@login_required
def Auto():
    search_term = request.args.get('term', '')
    res = Personal.query.filter(Personal.nombre.ilike(f'%{search_term}%'),Personal.active == 'Y').all()
    sugerencia = [personal.nombre for personal in res]
    return jsonify(sugerencia)

@ingreso.route('/ingreso/bita', methods=['GET'])
@login_required
def Auto2():
    search_term = request.args.get('term', '')
    res = Seguimiento.query.filter(Seguimiento.bitacora_expediente.ilike(f'{search_term}%'),Seguimiento.tipo_ingreso == 1).all()
    sugerencia = [{'bitacora_expediente':seguimiento.bitacora_expediente,
                   'rnomrazonsolcial':seguimiento.rnomrazonsolcial,
                   'materia':seguimiento.materia,
                   'tramite':seguimiento.tramite,
                   'turnado_da':seguimiento.turnado_da,
                   'procedencia':seguimiento.cve_procedencia,
                   'cadena_valor':seguimiento.cadena_valor,
                   'tipopersona':seguimiento.tipopersonalidad,
                   'dg':seguimiento.dirgralfirma
                   } for seguimiento in res]
    return jsonify(sugerencia)