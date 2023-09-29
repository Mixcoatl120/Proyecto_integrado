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