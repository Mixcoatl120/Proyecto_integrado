$(document).ready(function () {
    $('#mat').change(function () {
        var materia_id = $(this).val();
        if (materia_id) {
            $.ajax({
                url: '/ingreso/' + materia_id,
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $('#tra').empty();
                    $('#tra').append($('<option>', {
                        value: '',
                        text: 'Selecciona Tramite'
                    }));
                    $.each(data, function (key, value) {
                        $('#tra').append($('<option>', {
                            value: value.cvetramite,
                            text: value.cofemer
                        }));
                    });
                }
            });
        } else {
            $('#tra').empty();
            $('#tra').append($('<option>', {
                value: '',
                text: 'Selecciona Tramite'
            }));
        }
    });
});

$(function () {
    $("#res").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/auto',
                dataType: 'json',
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

$(function () {
    $("#bit").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: '/ingreso/bita',
                dataType: 'json',
                data: {
                    term: request.term
                },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 5 // Numero minimo de caracteres antes de mostrar sugerencias
    });
});