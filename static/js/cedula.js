$(document).ready(function () {
    // Asocia el evento click al botón
    $("#borrar").click(function () {
        // Borra el contenido del campo de entrada
        $("#bit").val("");
        $("#inicial").val("");
        $("#final").val("");
    });
});