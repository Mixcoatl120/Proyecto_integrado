from flask import Blueprint,Flask,render_template,request,jsonify
from flask_login import login_required
from app.dbModel import *


turnado_u = Blueprint('turnado_u',__name__,template_folder = 'templates')

@turnado_u.route('/turnado_u')
@login_required
def Turnado():
    return render_template('tablaeditar_u.html')

@turnado_u.route('/search_u', methods=['GET'])
def Search():
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

@turnado_u.route('/cambios_u',methods=['GET'])
@login_required
def Cambios():
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
    else:
        fecha_formateada = "" # en caso de que no contenga una fecha regresa vacio
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
    return render_template('turnado_u.html',update=data,ti=ti,asu=asu,mat=mat,dirg=dirg,des=des,pro=pro,cad_val=cad_val,tp=tp,res=res)

@turnado_u.route('/actualizar_u',methods=['POST'])
@login_required
def Actualizar():
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
        if fecha != "":
            actualizar.fecha_documento = request.form['fd']
            
        else:
            actualizar.fecha_documento = None 

        actualizar.contrato_cnh = request.form['cnh']
        actualizar.permiso_cre = request.form['cre']
        actualizar.con_copia = request.form['cc']

        folio = bit
        db.session.commit()  # Guarda los cambios en la base de datos
    return render_template('actualizar_u.html',folio=folio)
