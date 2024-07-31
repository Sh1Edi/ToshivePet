//
$("document").ready(function(){
    $("#form1").submit(function(e){
        
        var email = $("#email").val();
        var clave = $("#password").val();

        var msj = "";
        let enviar = false;

        // Validar email
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            msj += "El email no es válido<br>";
            enviar = true;
        }

        // Validar clave
        var claveRegex = /^(?=.*[A-Z])(?=.*[a-z])[A-Za-z0-9]{8,14}$/;
        if (!claveRegex.test(clave)) {
            msj += "La clave no cumple con los requisitos: debe tener al menos una letra mayúscula, no se permiten caracteres especiales y debe estar entre 8 y 14 caracteres<br>";
            enviar = true;
        }

        if(enviar){
            e.preventDefault();
            $("#warnings").html(msj);
        }
        else{
            $("#warnings").html("Inicio de sesion exitoso");
        }

    });

});
