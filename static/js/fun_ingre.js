/*
Funciones ------------------------------------
*/
$(document).ready(function () {
    // Funcion para ocultar y mostrar tipo de asunto 
    $("#ti").change(function () {
        if ($(this).val() === "2") { // Si se selecciona "ASUNTO"
            $("#ta, #lta").show(1000);// muestra
        }
        else {
            $("#ta, #lta").hide(1000);// oculta
            $("#ta").val("0")
        }
    });
    // Funcion para el select de Materia que obtendra las opciones de tramite
    $('#mat').change(function () { // defines el elemento que usara esta funcion al momento de cambio
        var materia_id = $(this).val();
        if (materia_id) {
            $.ajax({
                url: '/ingreso/' + materia_id, // ruta en donde encontrara la funcion de python
                type: 'GET',// metodo que recopila la informacion
                dataType: 'json',// tipo de archivo que espera la funcion
                success: function (data) {
                    // Vaciar el select de las opciones adicionales, pero no las marcadas con "no-eliminar"
                    $('#tra option:not(.no-eliminar)').remove();
                    /*llenado del elemeto afectado */
                    $.each(data, function (key, value) {
                        $('#tra').append($('<option>', {
                            value: value.idtram,
                            text: value.cofemer
                        }));
                    });
                }
            });
        }
        else {
            // Vaciar el select si no se ha seleccionado una materia
            $('#tra').empty();
        }
    });
});
// Autocompletador para el input de bitacora relacion
$(function () {
    const rs = $("#rs");
    let datos = [];
    $("#bit").autocomplete({ // defines el input que usara esta funcion 
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/bita', // url en donde buscara "la funcion a realizar en python"
                dataType: 'json',// el tipo de archivo que espera recibir ajax para predecir
                data: {
                    term: request.term // datos con el termino que introduciomos
                },
                success: function (data) {
                    datos = data // uso del array para evitar la perdida de datos y que el select pueda acceder a los datos en la funcion 
                    // Extrae solo los valores de bitacora_expediente
                    const bitacoraValores = data.map(item => item.bitacora_expediente);
                    response(bitacoraValores);
                },
            });
        },
        minLength: 10, // Numero minimo de caracteres antes de mostrar sugerencias
        select: function (event, ui) {
            // Cuando el usuario selecciona una opción
            const valorSeleccionado = ui.item.value;
            // Buscar el objeto correspondiente en los datos
            const seleccion = datos.find(item => item.bitacora_expediente === valorSeleccionado);
            // Llenar el otro input con 'rnomrazonsolcial'
            if (seleccion) {
                console.log(seleccion)
                rs.val(seleccion.rnomrazonsolcial);
                $("#mat").val(seleccion.materia);// establece la opcion correspondiente materia
                $('#mat').change();// ejecuta la funcion de cambio de materia para que llene los datos al momento de seleccionar una opcion de autocompletado
                setTimeout(function () {// funcion de delay para dejar cargar mat .change
                    // Aquí el código que se tiene que ejecutar con retardo
                    $('#tra').val(seleccion.tramite);
                }, 1000)
                $('#pro').val(seleccion.procedencia);// establece la opcion correspondiente procedencia
                $('#cv').val(seleccion.cadena_valor);// establece la opcion correspondiente cadena de valor
                $('#tp').val(seleccion.tipopersona);// establece la opcion correspondiente tipo persona
                $('#dg').val(seleccion.dg);// establece la opcion correspondiente direccion general
                $('#res').val(seleccion.turnado_da);// establece la opcion correspondiente responsble
            }
        }
    });
});