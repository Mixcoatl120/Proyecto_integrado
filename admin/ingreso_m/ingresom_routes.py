from flask import Blueprint,Flask,request,render_template,flash,jsonify
from flask_login import login_required
import datetime
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
    return render_template('datos.html',ti=ti,asu=asu,mat=mat,dirg=dirg,des=des,pro=pro,cad_val=cad_val,tp=tp,res=res)

@login_required
@admin_required
@ingresom.route('/ingresom/datos',methods=['POST','GET'])
def Datos():
    ti = Tip_ing.query.filter_by(id = request.form['ti']).first() # consulta a tabla de tipo ingreso
    asu = Asunto.query.filter_by(id = request.form['ta']).first() # consulta a tabla de asunto
    mat = Materia.query.filter_by(id = request.form['mat']).first() # consulta a tabla de materia
    tra = Tramite.query.filter_by(idtram = request.form['tra']).first()
    des = Descripcion.query.filter_by(id = request.form['des']).first()# consulta a tabla de descripcion
    pro = Procedencia.query.filter_by(id = request.form['pro']).first()# consulta a tabla de procedencia
    cad_val = Cad_val.query.filter_by(id = request.form['cv']).first()# consulta a cadena de valor
    dirg = Dir_Gen.query.filter_by(cve_unidad=2,id = request.form['dg']).first()# consulta a direccion general
    tp = Tip_per.query.filter_by(idtpers = request.form['tp']).first()# Consulta a tabla de tipo persona
    res = Personal.query.filter_by(active = 'Y',idpers = request.form['res']).first()# Cpnsulta a tabla de personal

    return render_template('formulario.html',ti=ti,asu=asu,mat=mat,dirg=dirg,des=des,pro=pro,cad_val=cad_val,tp=tp,res=res,tra=tra)


@ingresom.route('/foliom',methods=['POST','GET'])
@login_required
@admin_required
def Folio():
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
        fecha_larga = fat.strftime("%Y/%m/%d %H:%M:%S")
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
                                  nomreplegal = pit,
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
                                  nomreplegal = pit,
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
                                  nomreplegal = pit,
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
                                  nomreplegal = pit,
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

        flash(f'Se ha agregado correctamente el: {folio}', 'success')  # Mensaje de éxito
    
    return render_template('formulario.html',folio=folio)