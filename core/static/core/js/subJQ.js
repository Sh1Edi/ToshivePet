$("document").ready(function() {
    $("#form1").submit(function(e) {
      
      // Datos en variables
      var nombre = $("#fullname").val();
      var email = $("#email").val();
      var telefono = $("#phone").val();
      var clave = $("#pass").val();
      var donacion = $("#donacion").val();
  
      var msj = "";
      let enviar = false;
  
      if (nombre.length < 8 || nombre.length > 30) {
        msj += "El nombre debe tener entre 8 y 30 caracteres<br>";
        enviar = true;
      }
  
      var letra = nombre.charAt(0);
      if (!esMayscula(letra)) {
        msj += "El nombre debe comenzar con mayuscula<br>";
        enviar = true;
      }
  
      if (email.length < 12 || email.length > 30) {
        msj += "El email debe tener entre 12 y 30 caracteres<br>";
        enviar = true;
      }
  
      if (!/^\d+$/.test(telefono)) {
        msj += "El telefono debe estar compuesto solo por numeros<br>";
        enviar = true;
      }
      if (clave.length < 8 || clave.length > 14) {
        msj += "La clave debe estar en un rango de 8 a 15 caracteres (Letras)<br>";
        enviar = true;
      }
  
      if (!/^\d+$/.test(donacion) || parseInt(donacion) < 1000) {
        msj += "Su donacion debe ser un valor numérico mayor o igual a $1.000<br>";
        enviar = true;
      }

      if (enviar) {
        e.preventDefault();
        $("#sub").html(msj);
      } else {
        $("#sub").html("Suscripcion exitosa");
        this.submit();
        // Aquí puedes enviar el formulario
        // Ejemplo:
        // this.submit();
      }
    });
  
    function esMayscula(letra) {
      if (letra === letra.toUpperCase()) {
        return true;
      } else {
        return false;
      }
    }
  });
  