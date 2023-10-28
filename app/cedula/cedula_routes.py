from flask import Blueprint,Flask,render_template,request,make_response
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from app.dbModel import *

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
    res = Seguimiento.query.filter_by(fsolicitud = '10/07/2023').all()

    buffer = BytesIO()
    
    # Crear un objeto PDF usando ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    # Agregar una imagen a la primera página
    imagen_path = 'app/static/img/asea.png'  # Ruta de la imagen en tu sistema

    # Agregar contenido a cada pagina
    for seguimiento in res : # Generar el numero de solicitudes
        # Agregar un rectángulo blanco como fondo
        c.drawImage(imagen_path, 80, 690, width=200, height=50)  # Coordenadas y dimensiones de la imagen
        c.drawString(350, 720, "Sistema de Seguimiento de Trámites")
        c.drawString(375, 700, "Unidad de Gestión Industrial")
        c.drawString(100, 650, f'Folio: {seguimiento.bitacora_expediente}')
        c.drawString(350, 650, f'Fecha ingreso: {seguimiento.fsolicitud}')
        c.drawString(275, 100, "ATENTAMENTE:")
        c.drawString(225, 80, "ÁREA ATENCIÓN A REGULADO")


        
        styles = getSampleStyleSheet()

        # tabla de 9x2
        data = [
            ['Tipo Ingreso', ''],
            ['Regulado', ''],
            ['Remitente', ''],
            ['Materia', ''],
            ['Descripción', ''],
            ['Contenido', Paragraph(seguimiento.contenido, styles['Normal'])],
            ['Dirección General', ''],
            ['Director de Área', ''],
            ['Observaciones', Paragraph(seguimiento.observaciones, styles['Normal'])]
        ]
        table = Table(data, colWidths=[100, 350], rowHeights=[50 for _ in range(9)])  # Establecer anchos de columna [1ra columna, 2da columna]
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                  ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                  ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                  ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        
        table.wrapOn(c, 0, 0) # no se que realice 
        table.drawOn(c, 100, 175)  # ajusta la posicion de la tabla en el documento

        if res:
            c.showPage() # añade una nueva pagina al documento temporal
            
    # Guardar el PDF en el bufer
    c.save()

    buffer.seek(0)
    return buffer.read()