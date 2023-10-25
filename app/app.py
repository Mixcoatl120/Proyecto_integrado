import re
from turtle import update
from flask import Flask, render_template, request, redirect, request_tearing_down, url_for, flash, send_file, jsonify
from flask_login import LoginManager,login_user, logout_user, login_required
import psycopg2
import datetime
from config import *
from Funciones import imp_excel

#modelos

from models.ModelUser import ModelUser # modelo de usuarios 
from models.dbModel import * # modelo de la base de datos


#entities
from models.entities.Users import User # entidad usuario

#estableciondo la conección.
def conexion():
    conn = psycopg2.connect(**db_config)
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jvm2OrrMd4QaRNHzvtgqfxyLir8' # llave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/siset'# conexion a la base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app) # inicializacion de la base
    
login_manager_app = LoginManager(app) # Configuracion de login
login_manager_app.login_view = "login" # 

# Funcion para mantener la sesion del usuario activo
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.pswd:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contrasena incorrecta")
                return render_template('auth/login.html')
        else:
            flash('usuario no encontrado')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('inicio/home.html')

@app.route('/ingreso/')
@login_required
def ingresos():
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

@app.route('/ingreso/<materia_id>')
@login_required
def opc(materia_id):
    tramites = Tramite.query.filter_by(cvetramite = materia_id).all()
    tramites = [{'idtram':t.idtram,
                 'cvetramite': t.cvetramite,
                 'cofemer':t.cofemer
                 } for t in tramites]
    return jsonify(tramites)

# predecir responsable
@app.route('/ingreso/auto', methods=['GET'])
@login_required
def auto():
    search_term = request.args.get('term', '')
    res = Personal.query.filter(Personal.nombre.ilike(f'%{search_term}%'),Personal.active == 'Y').all()
    sugerencia = [personal.nombre for personal in res]
    return jsonify(sugerencia)

@app.route('/ingreso/bita', methods=['GET'])
@login_required
def auto2():
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

@app.route('/turnado/')
@login_required
def turnado():
    return render_template('Tablas/tablaeditar.html')

@app.route('/search', methods=['GET'])
def search():
    bit = request.args.get('bit')
    results = (
        db.session.query(
            Seguimiento.fsolicitud,
            Tip_ing.tipo_ingreso,
            Seguimiento.bitacora_expediente,
            Seguimiento.rnomrazonsolcial,
            Materia.materia,
            Dir_Gen.siglas,
            Estatus.estatus
        )
        .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)
        .outerjoin(Materia, Seguimiento.materia == Materia.id)
        .outerjoin(Estatus, Seguimiento.estatus_tramite == Estatus.id)
        .outerjoin(Dir_Gen, Seguimiento.dirgralfirma == Dir_Gen.id)
        .filter(Seguimiento.bitacora_expediente.like(f'{bit}%'),Seguimiento.estatus_tramite == '1')
        .all()
    )
    data = []
    for result in results:
        fsolicitud, tipo_ingreso, bitacora_expediente, materia,rnomrazonsocial, siglas, estatus = result

        # Formatear fsolicitud como "dd/mm/aaaa"
        formatted_fsolicitud = fsolicitud.strftime('%d/%m/%Y')

        data.append({
            "fsolicitud": formatted_fsolicitud,
            "tipo_ingreso": tipo_ingreso,
            "bitacora_expediente": bitacora_expediente,
            "materia":materia,
            "rnomrazonsocial": rnomrazonsocial,
            "siglas": siglas,
        })

    return jsonify({'data': data})

@app.route('/cambios',methods=['GET'])
@login_required
def cambios():
    data = Seguimiento.query.get(request.args.get('bitacora')) # Obtiene la bitacora y los datos relacionados
    ti = Tip_ing.query.all() # consulta a tabla de tipo ingreso
    asu = Asunto.query.all() # consulta a tabla de asunto
    mat = Materia.query.all() # consulta a tabla de materia
    des = Descripcion.query.all()# consulta a tabla de descripcion
    pro = Procedencia.query.all()# consulta a tabla de procedencia
    cad_val = Cad_val.query.all()# consulta a cadena de valor
    dirg = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    tp = Tip_per.query.all()# Consulta a tabla de tipo persona
    res = Personal.query.filter_by(active = 'Y').all()# Consulta a tabla de personal

        # verifica que persona que ingresa externa no sea nulo o None 
    if data.personaingresa_externa != None:
        persona_ingresa = data.personaingresa_externa
    else :
        persona_ingresa = ""

    # Verifica si hay una fecha
    if data.fecha_documento != None:
        fecha_formateada = data.fecha_documento.strftime("%Y-%m-%d")# da formato a la fecha para que el navegador la pueda entender
        print(fecha_formateada)
    else:
        fecha_formateada = "" # en caso de que no contenga una fecha regresa vacio

    print(data.totaltrami_pago)
    # objeto JSON update
    data = {
        'bitacora_expediente':data.bitacora_expediente,
        'tipo_ingreso':data.tipo_ingreso,
        'tipo_asunto':data.tipo_asunto,
        'materia':data.materia,
        'tramite':data.tramite,
        'descripcion':data.descripcion,
        'procedencia':data.cve_procedencia,
        'clave_proyecto':data.clave_proyecto,
        'cadena_valor':data.cadena_valor,
        'razon_social':data.rnomrazonsolcial,
        'tipo_persona':data.tipopersonalidad,
        'persona_ingresa':persona_ingresa,
        'dg':data.dirgralfirma,
        'responsable':data.turnado_da,
        'llave_pago':data.llavepago,
        'tramites_total':data.totaltrami_pago,
        'cuota_pago':data.couta_pago,
        'monto_total':data.monto_total,
        'contenido':data.contenido,
        'observaciones':data.observaciones,
        'antecedentes':data.antecedente,
        'clave_documento':data.clave_documento,
        'fecha_documento':fecha_formateada,
        'cnh':data.contrato_cnh,
        'con_copia':data.con_copia,
        'permiso_cre':data.permiso_cre
    }
    print(data)
    return render_template('inicio/turnado.html',update=data,ti=ti,asu=asu,mat=mat,dirg=dirg,des=des,pro=pro,cad_val=cad_val,tp=tp,res=res)

@app.route('/actualizar',methods=['POST'])
@login_required
def actualizar():
    bit = request.form['bit']
    actualizar = Seguimiento.query.get(bit) # Obtiene la bitacora bitacora
    if not actualizar:
        return "Usuario no encontrado", 404
    else:
        #Actualiza los datos del usuario con los valores enviados en el cuerpo de la solicitud
        actualizar.tipo_ingreso = request.form['ti']
        actualizar.tipo_asunto = request.form['ta']
        actualizar.materia = request.form['mat']
        actualizar.tramite = request.form['tra']
        actualizar.descripcion = request.form['des']
        actualizar.cve_procedencia = request.form['pro']
        actualizar.clave_proyecto = request.form['cp']
        actualizar.cadena_valor = request.form['cv']
        actualizar.rnomrazonsolcial = request.form['rs']
        actualizar.tipopersonalidad = request.form['tp']
        actualizar.personaingresa_externa = request.form['pit']
        actualizar.dirgralfirma = request.form['dg']
        actualizar.turnado_da = request.form['res']
        actualizar.llavepago = request.form['llp']
        actualizar.totaltrami_pago = request.form['tt']
        actualizar.cuota_pago = request.form['cup']
        actualizar.monto_total = request.form['mot']
        actualizar.contenido = request.form['con']
        actualizar.observaciones = request.form['obs']
        actualizar.antecedente = request.form['ant']
        actualizar.clave_documento = request.form['cd']

        fecha = request.form['fd']
        print(fecha)
        # Verifica si hay una fecha
        if fecha == None:
            actualizar.fecha_documento = request.form['fd']
        else:
            actualizar.fecha_documento = None

        actualizar.contrato_cnh = request.form['cnh']
        actualizar.permiso_cre = request.form['cre']
        actualizar.con_copia = request.form['cc']

        folio = bit
        db.session.commit()  # Guarda los cambios en la base de datos
    return render_template('ingreso/guardar.html',folio=folio)


@app.route('/folio',methods=['POST'])
@login_required
def folio():
    if request.method == 'POST':
        # datos del formulario
        ti = request.form['ti']
        ta = request.form['ta']
        mat = request.form['mat']
        tra = request.form['tra']
        des = request.form['des']
        pro = request.form['pro']
        cp = request.form['cp']
        cv = request.form['cv']
        rs = request.form['rs']
        tp = request.form['tp']
        pit = request.form['pit']
        dg = request.form['dg']
        res = request.form['res']
        llp = request.form['llp']
        tt = request.form['tt']
        cup = request.form['cup']
        mot = request.form['mot']
        con = request.form['con']
        obs = request.form['obs']
        ant = request.form['ant']
        cd = request.form['cd']
        fd = request.form['fd']
        cnh = request.form['cnh']
        cc = request.form['cc']
        cre = request.form['cre']
        tec = request.form['tec']

        # Obtener la fecha actual
        fecha_actual = datetime.date.today()
        # Obtener fecha y hora
        fat = datetime.datetime.now()
        # Hora completa
        fecha_larga = fat.strftime("%d/%m/%y %H:%M:%S")
        # Obtener los últimos dos dígitos del año
        ao_corto = fecha_actual.year % 100
        # Imprimir la fecha con el mes y los últimos dos dígitos del año
        f = fecha_actual.strftime(f"%m/{ao_corto:02}")

        # subconsulta
        #         ||    Select     ||   MAX    ||        columnas             ||
        subquery = db.session.query(db.func.max(IngresoAsea.fecha_ingreso_siset)).subquery() # .subquery indica que sera una subconsulta para poder agregarla a la principal
    
        # Consulta principal 
        #       ||     select   ||     bitacora_folio     || where ||    fecha_ingreso_siset = subconsulta    ||order by ||  bitacora_folio         ||DESC || LIMIT                                
        query = db.session.query(IngresoAsea.bitacora_folio).filter(IngresoAsea.fecha_ingreso_siset == subquery).order_by(IngresoAsea.bitacora_folio.desc()).limit(1)
        result = query.scalar() # obtiene todas los resultados
        uld = int(result[:7]) + 1
        # folio
        folio = "0"+str(uld) +"/"+f

        if(tec != "admin"):
            if(fd != ""):
                # busca el id de la sesion iniciada
                idp = Personal.query.filter_by(login = tec).first()
                insert = Seguimiento(cve_unidad = 2,
                                  tipo_ingreso = ti,
                                  tipo_asunto = ta,
                                  materia = mat,
                                  tramite = tra,
                                  descripcion = des,
                                  bitacora_expediente = folio,
                                  cve_procedencia = pro,
                                  clave_proyecto = cp,
                                  cadena_valor = cv,
                                  rnomrazonsolcial = rs,
                                  tipopersonalidad = tp,
                                  personaingresa_externa = pit,
                                  dirgralfirma = dg,
                                  turnado_da = res,
                                  llavepago = llp,
                                  totaltrami_pago = tt,
                                  couta_pago = cup,
                                  monto_total = mot,
                                  contenido = con,
                                  persona_ingresa = idp.idpers,
                                  observaciones = obs,
                                  antecedente = ant,
                                  clave_documento = cd,
                                  fecha_documento = fd,
                                  contrato_cnh = cnh,
                                  con_copia = cc,
                                  permiso_cre = cre,
                                  fsolicitud = fecha_actual,
                                  fingreso_siset = fecha_larga,
                                  estatus_tramite = 1,
                                  situacionactualtram = 9
            )
            else:
                # busca el id de la sesion iniciada
                idp = Personal.query.filter_by(login = tec).first()
                insert = Seguimiento(cve_unidad = 2,
                                  tipo_ingreso = ti,
                                  tipo_asunto = ta,
                                  materia = mat,
                                  tramite = tra,
                                  descripcion = des,
                                  bitacora_expediente = folio,
                                  cve_procedencia = pro,
                                  clave_proyecto = cp,
                                  cadena_valor = cv,
                                  rnomrazonsolcial = rs,
                                  tipopersonalidad = tp,
                                  personaingresa_externa = pit,
                                  dirgralfirma = dg,
                                  turnado_da = res,
                                  llavepago = llp,
                                  totaltrami_pago = tt,
                                  couta_pago = cup,
                                  monto_total = mot,
                                  contenido = con,
                                  persona_ingresa = idp.idpers,
                                  observaciones = obs,
                                  antecedente = ant,
                                  clave_documento = cd,
                                  fecha_documento = None,
                                  contrato_cnh = cnh,
                                  con_copia = cc,
                                  permiso_cre = cre,
                                  fsolicitud = fecha_actual,
                                  fingreso_siset = fecha_larga,
                                  estatus_tramite = 1,
                                  situacionactualtram = 9
            )
        else:            
            if(fd != ""):
                insert = Seguimiento(cve_unidad = 2,
                                  tipo_ingreso = ti,
                                  tipo_asunto = ta,
                                  materia = mat,
                                  tramite = tra,
                                  descripcion = des,
                                  bitacora_expediente = folio,
                                  cve_procedencia = pro,
                                  clave_proyecto = cp,
                                  cadena_valor = cv,
                                  rnomrazonsolcial = rs,
                                  tipopersonalidad = tp,
                                  personaingresa_externa = pit,
                                  dirgralfirma = dg,
                                  turnado_da = res,
                                  llavepago = llp,
                                  totaltrami_pago = tt,
                                  couta_pago = cup,
                                  monto_total = mot,
                                  contenido = con,
                                  persona_ingresa = 0,
                                  observaciones = obs,
                                  antecedente = ant,
                                  clave_documento = cd,
                                  fecha_documento = fd,
                                  contrato_cnh = cnh,
                                  con_copia = cc,
                                  permiso_cre = cre,
                                  fsolicitud = fecha_actual,
                                  fingreso_siset = fecha_larga,
                                  estatus_tramite = 1,
                                  situacionactualtram = 9
            )
            else:
                insert = Seguimiento(cve_unidad = 2,
                                  tipo_ingreso = ti,
                                  tipo_asunto = ta,
                                  materia = mat,
                                  tramite = tra,
                                  descripcion = des,
                                  bitacora_expediente = folio,
                                  cve_procedencia = pro,
                                  clave_proyecto = cp,
                                  cadena_valor = cv,
                                  rnomrazonsolcial = rs,
                                  tipopersonalidad = tp,
                                  personaingresa_externa = pit,
                                  dirgralfirma = dg,
                                  turnado_da = res,
                                  llavepago = llp,
                                  totaltrami_pago = tt,
                                  couta_pago = cup,
                                  monto_total = mot,
                                  contenido = con,
                                  persona_ingresa = 0,
                                  observaciones = obs,
                                  antecedente = ant,
                                  clave_documento = cd,
                                  fecha_documento = None,
                                  contrato_cnh = cnh,
                                  con_copia = cc,
                                  permiso_cre = cre,
                                  fsolicitud = fecha_actual,
                                  fingreso_siset = fecha_larga,
                                  estatus_tramite = 1,
                                  situacionactualtram = 9
            )
        db.session.add(insert)
        db.session.commit()
        db.session.close()
    
    return render_template('ingreso/guardar.html',folio=folio)

@app.route('/cedula')
@login_required
def cedula():
    return render_template('cedula/cedula.html')

@app.route('/consulta',methods=['GET','POST'])
@login_required
def consulta():
    tip_ingr = Tip_ing.query.all() # consulta a tramite
    items = Materia.query.all()# consulta a materia
    dir_gen = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    return render_template('inicio/consulta.html',items=items,tip_ingr=tip_ingr,dir_gen=dir_gen)

@app.route('/tabla', methods=('GET','POST'))
@login_required
def users():
    con_tipoingreso = ""
    if request.method == 'POST':# verifica si el request es por medio de post 
        f1 = request.form['fecha_inicial']# variable de fecha inicial
        f2 = request.form['fecha_final']# variable de fecha final
        mat = request.form['materia']# variable de materia
        ti = request.form['ta']# variable con condiciones de tipo ingreso
        dg = request.form['dg']# variables con condiciones de direccion general
    conn = conexion()
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
    return render_template('tablas/tabla.html', users=users)

@app.route('/download') # ruta para descargar el archivo xlsx de consulta
@login_required
def Download_File():
    #ruta para descargar el archivo
    PATH='source/Consulta.xlsx'
    return send_file(PATH,as_attachment=True,)

@app.errorhandler(404) # Error 404 por si no encuentra la pagina
def page_not_found(e):
    return render_template('errors/404.html')

def status_401(error): # Error 401 en caso de no iniciar sesion 
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.register_error_handler(401,status_401)
    app.run()