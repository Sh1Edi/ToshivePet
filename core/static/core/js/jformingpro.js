$(document).ready(function(){
    $("#formingpro").submit(function(p){
        
        var iding = $("#idingp").val();
        var nombreing = $("#nombreingp").val();
        var stocking = $("#stockingp").val();
        var fotop =  $("#fotoingp").val();
        var descping = $("#descpingp").val();
        var precioing = $("#precioingp").val();
        
        var msj = "";
        let enviar = false;
        
        if(iding.trim().length < 4 || iding.trim().length >4){
            msj +="* El ID debe tener 4 digitos";
            enviar = true; 
        }
        iding = parseInt(iding);
        if(!iding){
            msj += "<br>* El ID debe ser un número"
            enviar = true;
        }
        var letra = nombreing.charAt(0);
        if(!esMayuscula(letra)){
            msj +="<br>* El nombre del producto debe comenzar con una letra mayúscula";
            enviar = true;
        }
        if(nombreing.trim().length < 4 || nombreing.trim().length >50){
            msj +="<br>* El nombre del producto debe tener entre 4 y 50 caracteres";
            enviar = true;
        }
        if(stocking <0){
            msj +="<br>* El Stock del producto no puede ser negativo"
            enviar = true;
        }
        if (descping.length < 4 ){
            msj +="<br>* La descripcion debe contener mas de 4 caracteres"
            enviar = true;
        }
        if(precioing == 0){
            msj +="<br>* El precio no puede ser 0"
            enviar = true;
        }
        if(precioing < 0){
            msj +="<br>* El precio no puede ser negativo"
            enviar = true;
        }
        if(enviar){
            p.preventDefault();
            $("#warnings").html(msj);
        }
        else{
            $("#warnings").html("Guardado con exito!");
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

});