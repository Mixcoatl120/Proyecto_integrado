
$(document).ready(function () {


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

