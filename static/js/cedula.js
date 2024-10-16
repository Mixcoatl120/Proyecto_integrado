$(document).ready(function() {
    $("#r_con").click(function() {
        // Mostrar el mensaje de carga y el spinner
        $("#loadingMessage").show();
        $("#spinner").show();
        
        // Deshabilitar el botón para evitar múltiples envíos
        $(this).attr("disabled", true);

        // Obtener los datos del formulario
        let formData = new FormData($("#miFormulario")[0]);

        // Realizar la solicitud POST para generar el PDF
        fetch('/generar_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())  // Obtener la respuesta como un Blob
        .then(blob => {
            // Crear una URL para el blob y asignarla al iframe
            let url = URL.createObjectURL(blob);
            $("#pdfViewer").attr("src", url);

            // Ocultar el mensaje de carga y el spinner
            $("#loadingMessage").hide();
            $("#spinner").hide();

            // Habilitar el botón nuevamente
            $("#r_con").attr("disabled", false);
        })
        .catch(error => {
            console.error('Error:', error);

            // Ocultar el mensaje de carga y el spinner
            $("#loadingMessage").hide();
            $("#spinner").hide();

            // Habilitar el botón nuevamente
            $("#r_con").attr("disabled", false);
        });
    });

    // Limpiar formulario
    $("#borrar").click(function() {
        $("#miFormulario")[0].reset();
        $("#pdfViewer").attr("src", "");  // Limpiar el iframe si es necesario
    });
});