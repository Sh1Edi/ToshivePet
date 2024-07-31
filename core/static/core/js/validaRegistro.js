$("document").ready(function() {
    $("#formRegistro").submit(function(e) {
      var nombreCompleto = $("#fullname").val();
      var email = $("#email").val();
      var telefono = $("#phone").val();
      var clave = $("#pass").val();
      var respuesta = $("#respuesta").val();
  
      var msj = "";
      let enviar = false;
  
      // Validación de nombre completo
      if (!/^[A-Z][a-zA-Z\s]*$/.test(nombreCompleto)) {
        msj += "El nombre debe comenzar con mayúscula y solo puede contener letras y espacios.<br>";
        enviar = true;
      }

      if (nombreCompleto.length > 20  || nombreCompleto.length < 3 ){
        msj += "El nombre debe contener mas de 3 caracteres y menos de 20.<br>";
        enviar = true;
      }
      
      // Validación de email
      if (!/^\S+@\S+\.\S+$/.test(email)) {
        msj += "El email no es válido.<br>";
        enviar = true;
      }
  
      // Validación de teléfono
      if (!/^[0-9]{8,14}$/.test(telefono)) {
        msj += "El teléfono debe contener solo números y tener entre 8 y 14 dígitos.<br>";
        enviar = true;
      }
  
      // Validación de clave
      if (!/^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{3,15}$/.test(clave)) {
        msj += "La clave debe contener al menos una mayúscula, un número y tener al menos 3 caracteres.<br>";
        enviar = true;
      }
  
      // Validación de respuesta
      if (!/^[A-Z][a-zA-Z\s]*$/.test(respuesta)) {
        msj += "La respuesta debe comenzar con mayúscula y solo puede contener letras y espacios.<br>";
        enviar = true;
      }
  
      if (enviar) {
        e.preventDefault();
        $("#warnings").html(msj);
      } else {
        // Llama a la función de validación de contraseñas
        var password = $("#pass").val();
        var confirmPassword = $("#pass2").val();
        if (!validatePassword(password, confirmPassword)) {
          e.preventDefault();
          $("#warnings").html("Las contraseñas no coinciden.");
        } else {
          $("#warnings").html("Registro exitoso");
        }
      }
    });
  
    // Función de validación de contraseñas
    function validatePassword(password, confirmPassword) {
      return password === confirmPassword;
    }
});
