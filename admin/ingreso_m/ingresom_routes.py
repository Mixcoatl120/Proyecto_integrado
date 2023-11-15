from flask import Blueprint,Flask,request,render_template,jsonify
from flask_login import login_required
from login.login_routes import admin_required
from dbModel import *

ingresom = Blueprint('ingresom',__name__,template_folder = 'templates')

@login_required
@admin_required
@ingresom.route('/ingresom')
def Ingresom():
    ti = Tip_ing.query.all() # consulta a tabla de tipo ingreso
    asu = Asunto.query.all() # consulta a tabla de asunto
    mat = Materia.query.all() # consulta a tabla de materia
    des = Descripcion.query.all()# consulta a tabla de descripcion
    pro = Procedencia.query.all()# consulta a tabla de procedencia
    cad_val = Cad_val.query.all()# consulta a cadena de valor
    dirg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    tp = Tip_per.query.all()# Consulta a tabla de tipo persona
    res = Personal.query.filter_by(active = 'Y').all()# Cpnsulta a tabla de personal
    return render_template('formulario.html',ti=ti,asu=asu,mat=mat,des=des,pro=pro,cad_val=cad_val,dirg=dirg,tp=tp,res=res)