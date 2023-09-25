//codigo de javascript

var Smat = document.getElementById('mat');
var Stra = document.getElementById('tra');



Smat.addEventListener("change", function () {
    if (Smat.value == 1) {
        Stra.innerHTML = ''
        Stra.options.add(new Option("A","A"))
        Stra.options.add(new Option("B","B"))
    }
    if (Smat.value == 2) {
        Stra.innerHTML = ''
        Stra.options.add(new Option("C", "C"))
        Stra.options.add(new Option("D", "D"))
    }
});