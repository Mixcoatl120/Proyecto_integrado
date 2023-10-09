/*
Objetos del DOM
*/
$(document).ready(function () {
    $("#ti").change(function () {
        if ($(this).val() === "2") { // Si se selecciona "ASUNTO"
            console.log($("#ti").val());
            console.log("si");
            $("#ta, #lta").show(1000);
        }
        else {
            console.log("no");
            console.log($("#ti").val());
            $("#ta, #lta").hide(1000);
        }
    });
    /*
    Funcion para el select de Materia que obtendra las opcciones de tramite
    */
    $('#mat').change(function () { // defines el elemento que usara esta funcion
        var materia_id = $(this).val();
        if (materia_id) {
            $.ajax({
                url: '/ingreso/' + materia_id, // ruta en donde encontrara la funcion de python
                type: 'GET',// metodo que recupila la informacion
                dataType: 'json',// tipo de archivo que espera la funcion
                success: function (data) {
                    $('#tra').empty(); // Elemento que sera afectado 
                    $('#tra').append($('<option>', {// Elemento que sera llenado de opcciones
                        value: '',
                        text: 'Selecciona Tramite'
                    }));
                    /*llenado del elemeto afectado */
                    $.each(data, function (key, value) {
                        $('#tra').append($('<option>', {
                            value: value.cvetramite,
                            text: value.cofemer
                        }));
                    });
                }
            });
        } else {
            /*
            Si no me falla este es en caso de no seleccionar alguna opccion en Materia 
            */
            $('#tra').empty();
            $('#tra').append($('<option>', {
                value: '',
                text: 'Selecciona Tramite'
            }));
        }
    });
});
/*
Autocompletador para el input de responsable
*/
$(function () {
    $("#res").autocomplete({ // defines el input que usara esta funcion
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/auto', // url en donde buscara "la funcion a realizar en python"
                dataType: 'json',// el tipo de archivo que espera recibir ajax para predecir
                data: {
                    term: request.term
                },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 2 // Numero minimo de caracteres antes de mostrar sugerencias
    });
});

/*
Autocompletador para el input de bitacora relacion
*/
$(function () {
    const rs = $("#rs");
    let datos = [];
    $("#bit").autocomplete({ // defines el input que usara esta funcion 
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/bita', // url en donde buscara "la funcion a realizar en python"
                dataType: 'json',// el tipo de archivo que espera recibir ajax para predecir
                data: {
                    term: request.term 
                },
                success: function (data) {
                    datos = data
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
                rs.val(seleccion.rnomrazonsolcial);
                $("#mat").val(seleccion.materia);
                $('#mat').change();
            }
        }
    });
});