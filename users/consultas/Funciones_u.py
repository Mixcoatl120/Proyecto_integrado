﻿import pandas as pd
from flask_login import current_user #obtine el nombre de la sesión actual
import openpyxl

def imp_excel(con_where,uri_database):
    # sentencia inicial
    query = "SELECT" + \
        " seguimiento.fsolicitud," + \
    " cat_tipo_ingreso.tipo_ingreso," + \
    " cat_tipo_asunto.tipo," + \
    " cat_descripcion.descripcion," + \
    " cat_materia.materia," + \
    " cat_tramites.cofemer," + \
    " seguimiento.bitacora_expediente," + \
    " seguimiento.rnomrazonsolcial," + \
    " seguimiento.rfc," + \
    "seguimiento.nomreplegal," + \
    " seguimiento.permiso_cre," + \
    " seguimiento.clave_proyecto," + \
    " cat_tipoinstalacion.tipo_instalacion," + \
    " cat_actividad.actividad," + \
    " dir_gral.siglas," + \
    " seguimiento.fasigevaluador, " + \
    " evaluador.nombre,"+ \
    " seguimiento.contenido," + \
    " seguimiento.observaciones," + \
    " seguimiento.clave_documento,"+ \
    " seguimiento.fecha_documento,"+ \
    " seguimiento.numofapercb,"+ \
    " seguimiento.foficioaprcb,"+ \
    " seguimiento.fnotifapercb,"+ \
    " seguimiento.fdeshapercb,"+ \
    " seguimiento.numofpreve,"+ \
    " seguimiento.foficioprevencion,"+ \
    " seguimiento.fnotificacionprev,"+ \
    " seguimiento.fdesahogoprev,"+ \
    " seguimiento.noficiosolinfadic,"+ \
    " seguimiento.foficiosolinfadic,"+ \
    " seguimiento.fnotifsolinfadic,"+ \
    " seguimiento.fdesahsolinfadic,"+ \
    " seguimiento.nresolucion_ofresptram,"+ \
    " seguimiento.fresol_ofresptatram,"+ \
    " seguimiento.fnotificacionresol,"+ \
    " cat_sentido_resolucion.sentido_resolucion,"+ \
    " cat_estatus.estatus,"+\
    " cat_sitact.situacion_actual"+\
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
    #sentencia inicial con las condiciones ya integradas
    final = query + " " + con_where
    dataframe = pd.read_sql_query(final, uri_database)
    # guardando los datos en el excel
    excel_file_path = f'doc/Consulta{current_user.login}.xlsx'
    #encabezados(alias)
    alias =["FECHA DE INGRESO",
    "TIPO DE INGRESO",
    "TIPO DE ASUNTO",
    "DESCRIPCION",
    "MATERIA",
    "TRAMITE",
    "BITACORA",
    "RAZON SOCIAL",
    "RFC",
    "REPRESENTANTE LEGAL",
    "PERMISO CRE",
    "CLAVE DE PROYECTO",
    "TIPO DE INSTALACION",
    "ACTIVIDAD",
    "DIRECCION GRAL. FIRMA",
    "FECHA ASIG. EVALUADOR",
    "EVALUADOR",
    "CONTENIDO",
    "OBSERVACIONES",
    "CLAVE DEL DOCUMENTO",
    "FECHA DEL DOCUMENTO",
    "FOLIO APERCEBIMIENTO",
    "FECHA FOLIO APERCEBIMIENTO",
    "FECHA NOTI. APERCEBIMIENTO",
    "FECHA DESAH. APERCEBIMIENTO",
    "FOLIO PREVENCION",
    "FECHA FOLIO PREVENCION",
    "FECHA FOLIO PREVENCION",
    "FECHA DESAH. PREVENCION",
    "FOLIO INFO. ADICIONAL",
    "FECHA FOLIO INFO. ADICIONAL",
    "FECHA NOTI. INFO. ADICIONAL",
    "FECHA DESAH. INFO. ADICIONAL",
    "FOLIO RESOLUCION",
    "FECHA FOLIO RESOLUCION",
    "FECHA NOTIFI. RESOLUCION",
    "SENTIDO RESOLUCION",
    "ESTATUS",
    "SITUACION ACTUAL"]
    dataframe.to_excel(excel_file_path,header=alias ,index=False, engine='openpyxl')
