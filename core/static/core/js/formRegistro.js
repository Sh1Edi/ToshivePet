const formRegistro = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	usuario: /^[a-zA-Z0-9\s\_\-]{4,16}$/, // Letras, numeros, guion, guion_bajo y espacios

	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion, guion_bajo y sin espacios
	
	//nombre : /^[A-Z][a-zA-Z\s]{3,20}$/,
	nombre: /^[a-zA-ZÀ-ÿ\s]{2,40}$/, // Letras y espacios, pueden llevar acentos.
	password : /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{4,15}$/, // 4 a 15 digitos + numeros pd: al menos una letra debe ser mayuscula (si o si)
	//password: /^.{4,12}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/, // 7 a 14 numeros.	
	respuesta: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, 
}

const campos = {
	nombre : false, 
	correo : false,
	telefono : false,
	password : false,
	respuesta : false,
}

const validarFormulario = (e) => {
	//console.log('Se ejecuto')
	//console.log(e.target.name); -> nos muestra el nombre del input que se esta ejecutando
	switch (e.target.name) {
		case "nombre":
			//console.log('Funciona');
			// expresiones.x	-> esto es el diccionario de expresiones de arriba 
			// e.target -> es el input que recibio el evento
			// campo	-> es el nombre del input
			validarCampo(expresiones.usuario, e.target, 'nombre');
		break;

		case "correo":
			validarCampo(expresiones.correo, e.target, 'correo');
		break;

		case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;

		case "password":
			validarCampo(expresiones.password, e.target, 'password');
			validarPassword2();
		break;

		case "password2":
			validarPassword2();
		break;

		case "respuesta":
			validarCampo(expresiones.respuesta, e.target, 'respuesta')
		break;
	}
}


const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		//el e.target.value nos entrega el valor actual del input
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		// el "i" es la etiqueta del icono
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle')
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-xmark')
		//comentario
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');

		// el diccionario campos de arriba, esto es para validar que los campos esten rellenos
		// en el caso de que lo esten, cambia su valor a true, por lo tanto significa que esta escrito correctamente.
		campos[campo] = true;
	} else{
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		// el "i" es la etiqueta del icono
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-xmark')
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle')
		//Comentario
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}

const validarPassword2 = () => {
	const inputPassword1 = document.getElementById('password');
	const inputPassword2 = document.getElementById('password2');
	
	if(inputPassword1.value !== inputPassword2.value){
		document.getElementById(`grupo__password2`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-correcto');
		// el "i" es la etiqueta del icono
		document.querySelector(`#grupo__password2 i`).classList.add('fa-circle-xmark')
		document.querySelector(`#grupo__password2 i`).classList.remove('fa-check-circle')
		//Comentario
		document.querySelector(`#grupo__password2 .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos['password'] = false;
	} else {
		document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__password2`).classList.add('formulario__grupo-correcto');
		// el "i" es la etiqueta del icono
		document.querySelector(`#grupo__password2 i`).classList.remove('fa-circle-xmark')
		document.querySelector(`#grupo__password2 i`).classList.add('fa-check-circle')
		//Comentario
		document.querySelector(`#grupo__password2 .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos['password'] = true;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario)
});

formRegistro.addEventListener('submit', (e) => {
	//e.preventDefault(); -> evita que se envien los datos/ Cancela el evento submit
	//evita que la pagina envie el formulario sin datos

	// El siguiente If es para comprobar que los datos sean correctos

	if(campos.nombre && campos.correo && campos.telefono && campos.password && campos.respuesta){
		
		
		/* ESTA FORMA FUNCIONA
		swal.fire({
			icon: "success",
			title: "Registro exitoso",
			timer: 7000,
			showConfirmButton: false,
		})
		*/

		//formulario.reset();
		/*
		document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo');
		setTimeout(() => {
			//cuando pasen 5 segundos el mensaje se eliminara
			
			document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo');
		}, 5000)

		document.querySelectorAll('.formulario__grupo-correcto').forEach((icono) => {
			icono.classList.remove('formulario__grupo-correcto');
		})*/
		

	} else {
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
		setTimeout(() => {
			document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
		}, 5000)
		e.preventDefault();
	}

})