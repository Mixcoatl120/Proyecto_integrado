// JavaScript source code
var boton = document.getElementById('r_con');
var checks = document.querySelectorAll('.form-check-input');
var tip_asunto = "";
var tip_dir_gen = "";
boton.addEventListener('click', function () {
    checks.forEach((e) => {
        if (e.checked == true) {
            //if para separar  tipo de ingreso de los checksbox
            if (e.value == "ASUNTO" || e.value == "TRAMITE") {
                if (tip_asunto == "") {
                    tip_asunto = "and (cat_tipo_ingreso.tipo_ingreso = '" + e.value + "'";
                }
                else {
                    tip_asunto = tip_asunto + " or cat_tipo_ingreso.tipo_ingreso = '" + e.value + "'";
                }
            }

            //if para separar direccion general de los checksbox
            if (e.value != "ASUNTO" && e.value != "TRAMITE") {
                if (tip_dir_gen == "") {
                    tip_dir_gen = "and (dir_gral.siglas = '" + e.value + "'";
                }
                else {
                    tip_dir_gen = tip_dir_gen + " or dir_gral.siglas = '" + e.value + "'";
                }   
            }

        }
    });
    //llenado de los inputs ocultos 
    document.getElementById('con_tip').value = tip_asunto;
    document.getElementById('con_dg').value = tip_dir_gen;
});