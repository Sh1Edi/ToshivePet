var nombrepro = document.getElementById("nombrep"); 
var preciopro = document.getElementById("preciop");
var descripcionpro = document.getElementById("descp");

const formulario = document.getElementById("formedit");

var mensaje = document.getElementById("warnings");

formulario.addEventListener('submit', e =>{
    
    let msj = "";
    let enviar = false;

    if(nombrepro.value.length < 4 || nombrepro.value.length > 50){
        msj = msj + "* El nombre debe estar entre 4 y 50 caracteres";
        enviar = true;

    }

    var letra = nombrepro.value.charAt(0);
    console.log(letra);
    if(!esMayuscula(letra)){
        msj += "<br>Debe comenzar con una letra mayúscula";
        enviar = true;
    }

    if(enviar){
        e.preventDefault();
        mensaje.innerHTML = msj;
    }
    else{
        mensaje.innerHTML = "Enviado";
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