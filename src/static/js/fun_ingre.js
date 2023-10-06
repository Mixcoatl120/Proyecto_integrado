/*
Objetos del DOM
*/

const Sti = document.getElementById("ti")
console.log(Sti)

$(document).ready(function () {
    $('#ti').change(function () {
        var selectedValue = $('#ti').val();
        console.log(selectedValue)
        if (selectedValue == 2) {
            console.log("si");
            $('#ta').css('display', 'block');
        } else {
            console.log("no");
        }
    });
});
/*
Funcion para el select de Materia que obtendra las opcciones de tramite
*/
$(document).ready(function () {
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
    const inputOtro = $("#rs");
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
            const objetoSeleccionado = datos.find(item => item.bitacora_expediente === valorSeleccionado);
            // Llenar el otro input con 'rnomrazonsolcial'
            if (objetoSeleccionado) {
                console.log(objetoSeleccionado)
                inputOtro.val(objetoSeleccionado.rnomrazonsolcial);
            }
        }
    });
});