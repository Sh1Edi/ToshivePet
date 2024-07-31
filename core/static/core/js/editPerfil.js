
$("document").ready(function() {
    $("#formCambioPerfil").submit(function(e){
        var nombre = $("#nombre").val();
        var pass = $("#pass").val();
        var phone = $("#phone").val();

        var msj = "";
        let enviar = false;

        if (!/^[A-Z][a-zA-Z\s]*$/.test(nombre)) {
            msj += "El nombre debe comenzar con mayúscula y solo puede contener letras y espacios.<br>";
            enviar = true;
          }

        if (nombre.length > 20  || nombre.length < 3 ){
            msj += "El nombre debe contener mas de 3 caracteres y menos de 20.<br>";
            enviar = true;
          }

        if (!/^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{3,15}$/.test(pass)) {
            msj += "La clave debe contener al menos una mayúscula, un número y tener al menos 3 caracteres<br>";
            enviar = true;
        }

        if (!/^[0-9]{8,14}$/.test(phone)) {
            msj += "El teléfono debe contener solo números y tener entre 8 y 14 dígitos.<br>";
            enviar = true;
        }

        if(enviar){
            e.preventDefault();
            $("#warnings").html(msj);
        }
        else{
            $("#warnings").html("Perfil editado correctamente");
        }

    });
    
});
