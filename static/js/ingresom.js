$(document).ready(function () {
    // Selecciona el elemento select por su ID
    var selectElement = $('#ti');

    // Verifica si el valor de tipo ingreso es de 2 
    if (selectElement.val() === "2") {
        // El select tiene un valor seleccionado
        $("#ta, #lta").show(1000);// muestra
    } else {
        // El select no tiene un valor seleccionado
        $("#ta, #lta").hide(1000);// oculta
        $("#ta").val("0");
    }

    $('#tt').on('change', function () {
        // Check if the value is null or empty
        if (!$(this).val()) {
            // If empty, set the value to 0
            $(this).val(0);
        }
    });


    // calculo de monto 
    $('#tt, #cup').on('input', function () {
        // Obtener los valores de tt y cup y convertirlos a números
        var ttValue = parseFloat($('#tt').val()) || 0;
        var cupValue = parseFloat($('#cup').val()) || 0;

        // Calcular la suma de tt y cup
        var suma = ttValue * cupValue;

        // Actualizar el campo mot con el resultado
        $('#mot').val(suma.toFixed(2)); // Usar toFixed(2) para mostrar dos decimales
    });
});