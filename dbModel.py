"""Este .py contiene los modelos de las bases de datos o mas bien dicho las tablas que 
usara nuestro programa se tiene que definir con las columnas que usaremos de cada tabla
o definir toda la tabla 
nota: tiene que ser el mismo nombre de la columna de la base de datos para que pueda
realizar la sentencia SQL de manera correcta.
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tip_ing(db.Model): #------------------tipo ingreso----------------------
    __tablename__ = 'cat_tipo_ingreso'
   
    id = db.Column(db.Integer, primary_key=True)
    tipo_ingreso = db.Column(db.String(255))
    
    def __init__(self,id,tipo_ingreso):
        self.id = id
        self.tipo_ingreso = tipo_ingreso

class Asunto(db.Model): #------------------tipo asunto----------------------
    __tablename__ = 'cat_tipo_asunto'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255))
    
    def __init__(self,id,tipo):
        self.id = id
        self.tipo = tipo

class Materia(db.Model): #------------------Materia----------------------
    __tablename__ = 'cat_materia'

    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(255))
    
    def __init__(self,id,materia):
        self.id = id
        self.materia = materia

class Tramite(db.Model): #------------------Tramite----------------------
    __tablename__ = 'cat_tramites'

    idtram = db.Column(db.Integer, primary_key=True)
    cvetramite = db.Column(db.String(255))
    cofemer = db.Column(db.String(255))
    
    def __init__(self,idtram,cvetramite,cofemer):
        self.idtram = idtram
        self.cvetramite = cvetramite
        self.cofemer = cofemer

class Descripcion(db.Model): #------------------Descripcion----------------------
    __tablename__ = 'cat_descripcion'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255))

    def __init__(self,id,descripcion):
        self.id = id
        self.descripcion = descripcion

class Procedencia(db.Model): #------------------Procedencia----------------------
    __tablename__ = 'cat_procedencia'

    id = db.Column(db.Integer, primary_key=True)
    procedencia = db.Column(db.String(255))

    def __init__(self,id,procedencia):
        self.id = id
        self.procedencia = procedencia

class Cad_val(db.Model): #------------------Cadena de Valor----------------------
    __tablename__ = 'cat_cadena_valor'

    id = db.Column(db.Integer, primary_key=True)
    cadena_valor = db.Column(db.String(255))

    def __init__(self,id,cadena_valor):
        self.id = id
        self.cadena_valor = cadena_valor

class Tip_per(db.Model): #------------------Tipo persona----------------------
    __tablename__ = 'cat_tipopersona'

    idtpers = db.Column(db.Integer, primary_key=True)
    tipo_persona = db.Column(db.String(255))

    def __init__(self,idtpers,tipo_persona):
        self.idtpers = idtpers
        self.tipo_persona = tipo_persona

class Dir_Gen(db.Model): #------------------Direccion general----------------------
    __tablename__ = 'cat_dirgeneral'

    id = db.Column(db.Integer, primary_key=True)
    direccion_general = db.Column(db.String(255))
    siglas = db.Column(db.String(255))
    cve_unidad = db.Column(db.Integer)
    
    def __init__(self,id,direccion_general,siglas,cve_unidad):
        self.id = id
        self.direccion_general = direccion_general
        self.siglas = siglas
        self.cve_unidad = cve_unidad

class Personal(db.Model): #------------------Personal----------------------
    __tablename__ = 'cat_personal'

    idpers = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    active = db.Column(db.String(2))
    login = db.Column(db.String(50))
    
    def __init__(self,idpers,nombre,active,login):
        self.idpers = idpers
        self.nombre = nombre
        self.active = active
        self.login = login
               
class Seguimiento(db.Model): #------------------Seguimiento----------------------
    __tablename__ = 'seguimiento'

    cve_unidad = db.Column(db.Integer)
    tipo_ingreso = db.Column(db.Integer)
    tipo_asunto = db.Column(db.Integer)
    materia = db.Column(db.Integer)
    tramite = db.Column(db.Integer)
    descripcion = db.Column(db.Integer)
    bitacora_expediente = db.Column(db.String(100), primary_key=True)
    cve_procedencia = db.Column(db.Integer)
    clave_proyecto = db.Column(db.String(100))
    cadena_valor = db.Column(db.Integer)
    rnomrazonsolcial = db.Column(db.String(255))
    tipopersonalidad = db.Column(db.Integer)
    dirgralfirma = db.Column(db.Integer)
    turnado_da = db.Column(db.Integer)
    llavepago = db.Column(db.String(100))
    totaltrami_pago = db.Column(db.Integer)
    couta_pago = db.Column(db.String(64))
    monto_total = db.Column(db.String(64))
    contenido = db.Column(db.Text)
    persona_ingresa = db.Column(db.Integer)
    observaciones = db.Column(db.Text)
    antecedente = db.Column(db.String(512))
    clave_documento = db.Column(db.String(128))
    fecha_documento = db.Column(db.Date)
    contrato_cnh = db.Column(db.String(64))
    con_copia = db.Column(db.Text)
    permiso_cre = db.Column(db.String(64))
    fsolicitud = db.Column(db.Date)
    fingreso_siset = db.Column(db.Date)
    estatus_tramite = db.Column(db.Integer)
    situacionactualtram = db.Column(db.Integer)
    nomreplegal = db.Column(db.String(255))



    
    def __init__(self,cve_unidad,bitacora_expediente,rnomrazonsolcial,tipo_ingreso,materia,
                 tramite,turnado_da,cve_procedencia,cadena_valor,
                 tipopersonalidad,dirgralfirma,descripcion,clave_proyecto,
                 contenido,persona_ingresa,observaciones,
                 antecedente,clave_documento,fecha_documento,con_copia,
                 fsolicitud,fingreso_siset,tipo_asunto,permiso_cre,llavepago,estatus_tramite,
                 totaltrami_pago,contrato_cnh,couta_pago,monto_total,situacionactualtram,nomreplegal):

        self.cve_unidad = cve_unidad
        self.tipo_ingreso = tipo_ingreso
        self.tipo_asunto = tipo_asunto
        self.materia = materia
        self.tramite = tramite
        self.descripcion = descripcion
        self.bitacora_expediente = bitacora_expediente
        self.cve_procedencia = cve_procedencia
        self.clave_proyecto = clave_proyecto
        self.cadena_valor = cadena_valor
        self.rnomrazonsolcial = rnomrazonsolcial
        self.tipopersonalidad = tipopersonalidad
        self.dirgralfirma = dirgralfirma
        self.turnado_da = turnado_da
        self.llavepago = llavepago
        self.totaltrami_pago = totaltrami_pago
        self.couta_pago = couta_pago
        self.monto_total = monto_total
        self.contenido = contenido
        self.persona_ingresa = persona_ingresa
        self.observaciones = observaciones
        self.antecedente = antecedente
        self.clave_documento = clave_documento
        self.fecha_documento = fecha_documento
        self.contrato_cnh = contrato_cnh
        self.con_copia = con_copia
        self.permiso_cre = permiso_cre
        self.fsolicitud = fsolicitud
        self.fingreso_siset = fingreso_siset
        self.estatus_tramite = estatus_tramite
        self.situacionactualtram = situacionactualtram
        self.nomreplegal = nomreplegal

class IngresoAsea(db.Model): #------------------------- vista_ingreso asea------------------
    __tablename__ = 'ingreso_asea'
    fecha_ingreso_siset = db.Column(db.Date)
    fecha_ingreso = db.Column(db.Date)
    bitacora_folio = db.Column(db.String, primary_key=True)
    unidad = db.Column(db.Integer)
    razon_social = db.Column(db.String(255))

class Sitactual(db.Model):#------------------------- Situacion actual------------------
    __tablename__ = 'cat_sitact'
    id = db.Column(db.Integer, primary_key=True)
    situacion_actual = db.Column(db.String(255))

    def __init__(self,id,situacion_actual):
        self.id = id
        self.situacion_actual = situacion_actual

class Estatus(db.Model):#------------------------- Estatus------------------
    __tablename__ = 'cat_estatus'
    id = db.Column(db.Integer, primary_key=True)
    estatus = db.Column(db.String(255))

    def __init__(self,id,estatus):
        self.id = id
        self.estatus = estatus

class Users(db.Model):
    __tablename__= 'admin_users'
    login = db.Column(db.String(32), primary_key=True)
    pswd = db.Column(db.String(32))
    name = db.Column(db.String(64))
    active = db.Column(db.String(1))
    id = db.Column(db.Integer)
    
    def __init__(self,id,login,pswd,name,active):
        self.id = id
        self.login = login
        self.pswd = pswd
        self.name = name
        self.active = active