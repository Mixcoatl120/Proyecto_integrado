from flask import Blueprint,Flask, redirect,render_template,request,make_response,flash
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from app.dbModel import *
from datetime import datetime
from app import admin_required

cedula = Blueprint('cedula',__name__,template_folder = 'templates')

def Nulos(a):
    if a == None or "":
        b = ""
    else:
        b = a
    return b
def Formato_fecha(a):
     # formato para fechas
    if a == None or a == "":
        fecha_formateada = None
    else:
        fecha_objeto = datetime.strptime(a,'%Y-%m-%d') # espera el formato mencionado del string para establecerla como fecha
        fecha_formateada = fecha_objeto.strftime('%d/%m/%Y') # cambia el formato de la fecha anterior a dd/mm/aaaa
    return fecha_formateada
def generar_archivo_pdf():
    from io import BytesIO
    inicial = request.form['inicial']
    final = request.form['final']
    bitacora = request.form['bit']
    
    # Valida que las fechas no esten vacias 
    inicial = Formato_fecha(inicial)
    final = Formato_fecha(final)

    # Verifica bitacora para saber cual query seleccionar
    if bitacora == None or bitacora == "":
        res = (
            db.session.query(
                Seguimiento.bitacora_expediente,
                Seguimiento.fsolicitud,
                Tip_ing.tipo_ingreso,
                Seguimiento.rnomrazonsolcial,
                Seguimiento.nomreplegal,
                Materia.materia,
                Descripcion.descripcion,
                Seguimiento.contenido,
                Dir_Gen.siglas,
                Personal.nombre, 
                Seguimiento.observaciones
            )
            .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)# left join
            .outerjoin(Materia, Seguimiento.materia == Materia.id)# left join
            .outerjoin(Descripcion, Seguimiento.descripcion == Descripcion.id)# left join
            .outerjoin(Estatus, Seguimiento.estatus_tramite == Estatus.id)# left join
            .outerjoin(Dir_Gen, Seguimiento.dirgralfirma == Dir_Gen.id)# left join
            .outerjoin(Personal, Seguimiento.turnado_da == Personal.idpers)# left join
            .filter( # where
                Seguimiento.fsolicitud >= inicial, 
                Seguimiento.fsolicitud <= final,
                Seguimiento.fingreso_siset != None
            )
            .order_by(Seguimiento.bitacora_expediente)# order by
            .all()
)
    else:
        res = (
            db.session.query(
                Seguimiento.bitacora_expediente,
                Seguimiento.fsolicitud,
                Tip_ing.tipo_ingreso,
                Seguimiento.rnomrazonsolcial,
                Seguimiento.nomreplegal,
                Materia.materia,
                Descripcion.descripcion,
                Seguimiento.contenido,
                Dir_Gen.siglas,
                Personal.nombre, 
                Seguimiento.observaciones
            )
            .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)# left join
            .outerjoin(Materia, Seguimiento.materia == Materia.id)# left join
            .outerjoin(Descripcion, Seguimiento.descripcion == Descripcion.id)# left join
            .outerjoin(Estatus, Seguimiento.estatus_tramite == Estatus.id)# left join
            .outerjoin(Dir_Gen, Seguimiento.dirgralfirma == Dir_Gen.id)# left join
            .outerjoin(Personal, Seguimiento.turnado_da == Personal.idpers)# left join
            .filter( # where
                Seguimiento.bitacora_expediente == bitacora,
                Seguimiento.fingreso_siset != None
            )
            .order_by(Seguimiento.bitacora_expediente)# order by
            .all()
            )
        
    buffer = BytesIO()
    # Crear un objeto PDF usando ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    # Agregar una imagen a la primera página
    imagen_path = 'app/static/img/asea.png'  # Ruta de la imagen en tu sistema


    # Agregar contenido a cada pagina
    for seguimiento in res : # Generar el numero de solicitudes
        fecha_f = seguimiento.fsolicitud.strftime('%d/%m/%Y') # formatea la fecha de los datos entrantes

        # funcion Nulos verifica que no tenga algun valor None o Nulo cada una de las variables
        tipo_ingreso = Nulos(seguimiento.tipo_ingreso)# tipo ingreso
        razon_social = Nulos(seguimiento.rnomrazonsolcial) # regulado
        persona_ingresae = Nulos(seguimiento.nomreplegal)# remitente
        materia = Nulos(seguimiento.materia)# materia
        descripcion = Nulos(seguimiento.descripcion)# descripcion
        contenido = Nulos(seguimiento.nombre)# contenido
        siglas = Nulos(seguimiento.siglas)# D.G
        nombre = Nulos(seguimiento.nombre)
        observaciones = Nulos(seguimiento.observaciones)# observaciones
        
        
        c.drawImage(imagen_path, 50, 700, width=285, height=65)  # Coordenadas y dimensiones de la imagen

        #             X   Y
        c.drawString(350, 750, "Sistema de Seguimiento de Trámites")
        c.drawString(375, 730, "Unidad de Gestión Industrial")
        c.drawString(50, 690, f'FOLIO: {seguimiento.bitacora_expediente}')
        c.drawString(385, 690, f'FECHA INGRESO: {fecha_f}')
        c.drawString(260, 70, "ATENTAMENTE:")
        c.drawString(200, 50, "ÁREA DE ATENCIÓN AL REGULADO")

        styles = getSampleStyleSheet()
        
        # Ajusta el tamaño del texto
        small_style = styles["Normal"]
        small_style.fontName = "Helvetica"  # tipo de fuente
        small_style.fontSize = 8  # tamaño de la letra 

        # tabla de 9x2
        data = [
            ['Tipo Ingreso', Paragraph(tipo_ingreso, small_style)],
            ['Regulado', Paragraph(razon_social, styles['Normal'])],
            ['Remitente', Paragraph(persona_ingresae, styles['Normal'])],
            ['Materia', Paragraph(materia, styles['Normal'])],
            ['Descripción', Paragraph(descripcion, styles['Normal'])],
            ['Contenido', Paragraph(contenido, styles['Normal'])],
            ['Dirección General', Paragraph(siglas, styles['Normal'])],
            ['Director de Área', Paragraph(nombre, styles['Normal'])],
            ['Observaciones', Paragraph(observaciones, styles['Normal'])]
        ]
        table = Table(data, colWidths=[100, 412], rowHeights=[60 for _ in range(9)])  # Establecer anchos de columna [1ra columna, 2da columna]
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # asigna el texto a la izquierda
            ('VALIGN', (0, 0), (-1, -1), 'TOP')  # asigna el texto en el top de la celda
        ]))
        
        table.wrapOn(c, 0, 0) # no se que realice 
        table.drawOn(c, 50, 125)  # ajusta la posicion de la tabla en el documento

        if res:
            c.showPage() # añade una nueva pagina al documento temporal
            
    # Guardar el PDF en el bufer
    c.save()

    buffer.seek(0)
    return buffer.read()
        

@cedula.route('/cedula')
@login_required
@admin_required
def Cedula():
    return render_template('cedula.html')

@cedula.route('/generar_pdf',methods =['POST'])
def generar_pdf():
    fecha = datetime.now().date()
    fecha_formateada = fecha.strftime('%d-%m-%Y') # cambia el formato de la fecha anterior a dd/mm/aaaa
    
    response = make_response(generar_archivo_pdf())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Turnado {fecha_formateada}.pdf'
    return response

