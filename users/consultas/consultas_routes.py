from flask import Blueprint,Flask,render_template,request,send_file
from flask_login import login_required,current_user
from dbModel import *
from users.consultas.Funciones_u import *
from config import db_config

consulta_u = Blueprint('consulta_u',__name__,template_folder = 'templates')
#estableciondo la conección.
def Conexion():
    conn = psycopg2.connect(**db_config)
    return conn

@consulta_u.route('/consulta_u',methods=['GET','POST'])
@login_required
def Consulta():
    tip_ingr = Tip_ing.query.all() # consulta a tramite
    items = Materia.query.all()# consulta a materia
    dir_gen = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    return render_template('consulta_u.html',items=items,tip_ingr=tip_ingr,dir_gen=dir_gen)

@consulta_u.route('/tabla_u', methods=('GET','POST'))
@login_required
def Users():
    con_tipoingreso = ""
    if request.method == 'POST':# verifica si el request es por medio de post 
        f1 = request.form['fecha_inicial']# variable de fecha inicial
        f2 = request.form['fecha_final']# variable de fecha final
        mat = request.form['materia']# variable de materia
        ti = request.form['ta']# variable con condiciones de tipo ingreso
        dg = request.form['dg']# variables con condiciones de direccion general
    conn = Conexion()
    cursor = conn.cursor()
    #consulta inicial esto es para la tabla que se visualiza en html 
    con_inicial = "SELECT" + \
    " seguimiento.fsolicitud," + \
    " cat_tipo_ingreso.tipo_ingreso," + \
    "seguimiento.bitacora_expediente," + \
    " cat_materia.materia," + \
    " seguimiento.rnomrazonsolcial," + \
    " dir_gral.siglas," + \
    " cat_estatus.estatus" + \
    " FROM seguimiento" + \
    " LEFT JOIN cat_tipo_ingreso ON seguimiento.tipo_ingreso = cat_tipo_ingreso.id" + \
    " LEFT JOIN cat_tipo_asunto ON seguimiento.tipo_asunto = cat_tipo_asunto.id" + \
    " LEFT JOIN cat_descripcion ON seguimiento.descripcion = cat_descripcion.id" + \
    " LEFT JOIN cat_materia ON seguimiento.materia = cat_materia.id" + \
    " LEFT JOIN cat_tramites ON seguimiento.tramite = cat_tramites.idtram" + \
    " LEFT JOIN cat_tipoinstalacion  ON seguimiento.tipoinstalacion = cat_tipoinstalacion.id" + \
    " LEFT JOIN cat_actividad ON seguimiento.cve_actividad = cat_actividad.id" + \
    " LEFT JOIN cat_personal AS evaluador ON seguimiento.nevaluador = evaluador.idpers" + \
    " LEFT JOIN cat_personal AS aar ON seguimiento.persona_ingresa = aar.idpers" +\
    " LEFT JOIN dir_gral ON seguimiento.dirgralfirma = dir_gral.id" + \
    " LEFT JOIN cat_sitact ON seguimiento.situacionactualtram = cat_sitact.id" + \
    " LEFT JOIN cat_sentido_resolucion ON seguimiento.sentido_resolucion = cat_sentido_resolucion.id" + \
    " LEFT JOIN cat_estatus ON seguimiento.estatus_tramite = cat_estatus.id" + \
    " WHERE"

    # string con la condicion de fecha
    con_fechas = "(seguimiento.fsolicitud >= " + "'" + f1 + "'" + " and seguimiento.fsolicitud <= " + "'" + f2 + "')"
    # string con condiciones tipo de ingreso
    if ti != "":
        con_tipoingreso = ti +")"
    # string con dicion de materia
    if mat != "TODO":
        con_materia = "and cat_materia.materia ='" + mat + "'"
    else:
        con_materia = ""
    # string con las condiciones de direccion general
    if dg !="":
        con_dirgeneral =dg + ")"
    else:
        con_dirgeneral = ""
    # string con la sentencia final completa
    query = con_inicial + " " + con_fechas + " " +con_tipoingreso + " " + con_materia + " " + con_dirgeneral
    # string con condiciones para la funcion de exportar excel
    con_where = con_fechas + " " +con_tipoingreso + " " + con_materia + " " + con_dirgeneral
    # funcion para realizar una consulta y crear un archivo en excel para su descarga
    imp_excel(con_where)
    #
    cursor.execute(query)
    users = cursor.fetchall()      
    conn.close()
    return render_template('tabla_u.html', users=users)

@consulta_u.route('/download_u') # ruta para descargar el archivo xlsx de consulta
@login_required
def Download_File():
    #ruta para descargar el archivo
    PATH=f'doc/Consulta{current_user.login}.xlsx'
    return send_file(PATH,as_attachment=True,)