from flask import Blueprint,Flask,render_template,request,make_response
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from app.dbModel import *
from datetime import datetime 

cedula = Blueprint('cedula',__name__,template_folder = 'templates')

@cedula.route('/cedula')
@login_required
def Cedula():
    return render_template('cedula.html')

@cedula.route('/generar_pdf',methods =['POST'])
def generar_pdf():
    response = make_response(generar_archivo_pdf())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=mi_archivo.pdf'
    return response

def generar_archivo_pdf():
    from io import BytesIO
    inicial = request.form['inicial']
    final = request.form['final']
    #bitacora = request.form['bit']
    
    # formato para fecha inicial
    fecha_objeto1 = datetime.strptime(inicial,'%Y-%m-%d') # espera el formato mencionado del string para establecerla como fecha
    fecha_formateada1 = fecha_objeto1.strftime('%d/%m/%Y') # cambia el formato de la fecha anterior a dd/mm/aaaa
    
    # formato para fecha final 
    fecha_objeto2 = datetime.strptime(final,'%Y-%m-%d') # espera el formato mencionado del string para establecerla como fecha
    fecha_formateada2 = fecha_objeto2.strftime('%d/%m/%Y') # cambia el formato de la fecha anterior a dd/mm/aaaa
    
    res = (
        db.session.query(
            Seguimiento.bitacora_expediente,
            Seguimiento.fsolicitud,
            Tip_ing.tipo_ingreso,
            # regulado
            # remitente
            Materia.materia,
            Descripcion.descripcion,
            Seguimiento.contenido,
            Dir_Gen.siglas,
            # director de area 
            Seguimiento.observaciones
        )
        .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)# left join
        .outerjoin(Materia, Seguimiento.materia == Materia.id)# left join
        .outerjoin(Descripcion, Seguimiento.descripcion == Descripcion.id)# left join
        .outerjoin(Estatus, Seguimiento.estatus_tramite == Estatus.id)# left join
        .outerjoin(Dir_Gen, Seguimiento.dirgralfirma == Dir_Gen.id)# left join
        .filter(
            Seguimiento.fsolicitud >= fecha_formateada1, 
            Seguimiento.fsolicitud <= fecha_formateada2,
            Seguimiento.estatus_tramite == '1'
            )# where
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
        
        # verifica que la descripcion no este vacia o sea nula
        if seguimiento.descripcion == None:
            descripcion = ""
        else:
            descripcion = seguimiento.descripcion
            
        # verifica que la contenido no este vacia o sea nula
        if seguimiento.contenido == None:
            contenido = ""
        else:
            contenido = seguimiento.descripcion
        
        # Agregar un rectángulo blanco como fondo
        c.drawImage(imagen_path, 50, 720, width=250, height=50)  # Coordenadas y dimensiones de la imagen
        c.drawString(350, 750, "Sistema de Seguimiento de Trámites")
        c.drawString(375, 730, "Unidad de Gestión Industrial")
        c.drawString(50, 690, f'FOLIO: {seguimiento.bitacora_expediente}')
        c.drawString(385, 690, f'FECHA INGRESO: {fecha_f}')
        c.drawString(275, 100, "ATENTAMENTE:")
        c.drawString(225, 80, "ÁREA ATENCIÓN A REGULADO")

        styles = getSampleStyleSheet()
        
        # Ajusta el tamaño del texto
        small_style = styles["Normal"]
        small_style.fontName = "Helvetica"  # tipo de fuente
        small_style.fontSize = 8  # tamaño de la letra 

        # tabla de 9x2
        data = [
            ['Tipo Ingreso', Paragraph(seguimiento.tipo_ingreso, small_style)],
            ['Regulado', ''],
            ['Remitente', ''],
            ['Materia', Paragraph(seguimiento.materia, styles['Normal'])],
            ['Descripción', Paragraph(descripcion, styles['Normal'])],
            ['Contenido', Paragraph(contenido, styles['Normal'])],
            ['Dirección General', Paragraph(seguimiento.siglas, styles['Normal'])],
            ['Director de Área', Paragraph('CHAVEZ HIKIYA ERENDIRA HANAKO', styles['Normal'])],
            ['Observaciones', Paragraph(seguimiento.observaciones, styles['Normal'])]
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