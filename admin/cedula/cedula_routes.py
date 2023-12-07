from flask import Blueprint,Flask, redirect,render_template,request,make_response,flash
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from dbModel import *
from datetime import datetime
from login.login_routes import admin_required

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
        fecha_formateada = fecha_objeto.strftime('%Y/%m/%d') # cambia el formato de la fecha anterior a dd/mm/aaaa
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
                Tramite.cofemer,
                Descripcion.descripcion,
                Seguimiento.contenido,
                Dir_Gen.siglas,
                Personal.nombre, 
                Seguimiento.observaciones
            )
            .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)# left join
            .outerjoin(Materia, Seguimiento.materia == Materia.id)# left join
            .outerjoin(Tramite, Seguimiento.tramite == Tramite.idtram)
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
                Tramite.cofemer,
                Descripcion.descripcion,
                Seguimiento.contenido,
                Dir_Gen.siglas,
                Personal.nombre, 
                Seguimiento.observaciones
            )
            .outerjoin(Tip_ing, Seguimiento.tipo_ingreso == Tip_ing.id)# left join
            .outerjoin(Materia, Seguimiento.materia == Materia.id)# left join
            .outerjoin(Tramite, Seguimiento.tramite == Tramite.idtram)
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
    imagen_path = 'static/img/asea.png'  # Ruta de la imagen en tu sistema


    # Agregar contenido a cada pagina
    for seguimiento in res : # Generar el numero de solicitudes
        fecha_f = seguimiento.fsolicitud.strftime('%d/%m/%Y') # formatea la fecha de los datos entrantes

        # funcion Nulos verifica que no tenga algun valor None o Nulo cada una de las variables
        tipo_ingreso = Nulos(seguimiento.tipo_ingreso)# tipo ingreso
        razon_social = Nulos(seguimiento.rnomrazonsolcial) # regulado
        persona_ingresae = Nulos(seguimiento.nomreplegal)# remitente
        materia = Nulos(seguimiento.materia)# materia
        tramite = Nulos(seguimiento.cofemer)# tramite
        descripcion = Nulos(seguimiento.descripcion)# descripcion
        contenido = Nulos(seguimiento.contenido)# contenido
        siglas = Nulos(seguimiento.siglas)# D.G
        nombre = Nulos(seguimiento.nombre)# director de area
        observaciones = Nulos(seguimiento.observaciones)# observaciones
        
        #                        x    y 
        c.drawImage(imagen_path, 15, 725, width=285, height=65)  # Coordenadas y dimensiones de la imagen

        # Definir el tipo de fuente y tamaño para los textos sueltos.
        c.setFont("Helvetica-Bold", 13)

        #             X   Y
        c.drawString(335, 765, "Sistema de Seguimiento de Trámites")
        c.drawString(360, 745, "Unidad de Gestión Industrial")
        c.drawString(40, 710, f'FOLIO: {seguimiento.bitacora_expediente}')
        c.drawString(385, 710, f'FECHA INGRESO: {fecha_f}')
        c.drawString(240, 60, "ATENTAMENTE:")
        c.drawString(180, 40, "ÁREA DE ATENCIÓN AL REGULADO")

        styles = getSampleStyleSheet()

        # Ajusta el tamaño del texto de la primera columna
        estilo_1_columna = styles["Heading1"]
        estilo_1_columna.fontName = "Helvetica-Bold"  # tipo de fuente
        estilo_1_columna.fontSize = 12 # tamaño de la letra 
        # Nota: para que cambie el tamaño de la fuente tienes que usar small_style no styles['Normal']
        
        # Ajusta el tamaño del texto de la segunda columna
        estilo_2_columna = styles["Normal"]
        estilo_2_columna.fontName = "Helvetica"  # tipo de fuente
        estilo_2_columna.fontSize = 10 # tamaño de la letra 
        # Nota: para que cambie el tamaño de la fuente tienes que usar small_style no styles['Normal']

        # tabla de 9x2
        data = [
            [Paragraph('Tipo De Ingreso', estilo_1_columna), Paragraph(tipo_ingreso, estilo_2_columna)],
            [Paragraph('Regulado', estilo_1_columna), Paragraph(razon_social, estilo_2_columna)],
            [Paragraph('Remitente', estilo_1_columna), Paragraph(persona_ingresae, estilo_2_columna)],
            [Paragraph('Materia', estilo_1_columna), Paragraph(materia, estilo_2_columna)],
            [Paragraph('Trámite', estilo_1_columna), Paragraph(tramite, estilo_2_columna)],
            [Paragraph('Descripción', estilo_1_columna), Paragraph(descripcion, estilo_2_columna)],
            [Paragraph('Contenido', estilo_1_columna), Paragraph(contenido, estilo_2_columna)],
            [Paragraph('Dirección General', estilo_1_columna), Paragraph(siglas, estilo_2_columna)],
            [Paragraph('Director De Área', estilo_1_columna), Paragraph(nombre, estilo_2_columna)],
            [Paragraph('Observaciones', estilo_1_columna), Paragraph(observaciones, estilo_2_columna)]
        ]
        table = Table(data, colWidths=[120, 412], rowHeights=[61 for _ in range(10)])  # Establecer anchos de columna [1ra columna, 2da columna]
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),# color del fondo
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),# color del texto
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # asigna el texto a la izquierda
            ('VALIGN', (0, 0), (-1, -1), 'TOP')  # asigna el texto en el top de la celda
        ]))
        
        table.wrapOn(c, 0, 0) # no se que realice 
        table.drawOn(c, 40, 85)  # ajusta la posicion de la tabla en el documento

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

