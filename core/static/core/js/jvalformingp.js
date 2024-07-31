var iding = document.getElementById("idingp");
var nombreing = document.getElementById("nombreingp");
var stocking = document.getElementById("stockingp");
var fotop = document.getElementsByClassName("fotoingp");
var descping = document.getElementById("descpingp");
var precioing = document.getElementById("precioingp");

const formulariop = document.getElementById("formingpro");

var mensaje = document.getElementById("warnings");

formulariop.addEventListener('submit', i =>{
    
    let msj = "";
    let enviar = false;

    if(idingp.value.length < 4 || idingp.value.length > 4){
            msj = msj + "El ID debe 4 digitos";
            enviar = true;
    }
    var letra = nombreing.value.charAt(0);
    console.log(letra);
    if(!esMayuscula(letra)){
        msj +="<br>El nombre del producto debe comenzar con una letra mayúscula";
        enviar = true;
    }
    if(nombreing.value.length < 4 || nombreing.value.length >50){
        msj +="El nombre debe del producto debe tener entre 4 y 50 caracteres";
        enviar = true;
    }
    if(enviar){
        i.preventDefault();
        mensaje.innerHTML = msj;
    }
    else{
        mensaje.innerHTML = "Guardado";
    }
});

function esMayuscula(letra){
    if(letra === letra.toUpperCase()){
        return true;
    }
    else{
        return false;
    }
}