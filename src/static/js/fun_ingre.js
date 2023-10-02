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
    $("#bit").autocomplete({ // defines el input que usara esta funcion 
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/bita', // url en donde buscara "la funcion a realizar en python"
                dataType: 'json',// el tipo de archivo que espera recibir ajax para predecir
                data: {
                    term: request.term 
                },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 10 // Numero minimo de caracteres antes de mostrar sugerencias
    });
});