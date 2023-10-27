from flask import Blueprint,Flask,render_template,request,make_response
from flask_login import login_required
from reportlab.lib.pagesizes import letter
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
    res = Seguimiento.query.filter_by(fsolicitud = '10/10/2023').all()

    buffer = BytesIO()
    

    # Crear un objeto PDF usando ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)

    # Agregar contenido a cada pagina
    for seguimiento in res : # Generar el numero de solicitudes
        c.drawString(100, 750, f'Folio:{seguimiento.bitacora_expediente}')

        if res:
            c.showPage()

    # Guardar el PDF en el bufer
    c.save()

    buffer.seek(0)
    return buffer.read()