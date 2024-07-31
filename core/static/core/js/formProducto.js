const formRegistro = document.getElementById('formingpro');
const inputs = document.querySelectorAll('#formingpro input');

const expresiones = {
    id: /^\d{1,14}$/, // 7 a 14 numeros.	
	nombre: /^[a-zA-ZÀ-ÿ\s]{2,40}$/, // Letras y espacios, pueden llevar acentos.
    stock : /^\d{1,20}$/, // 7 a 14 numeros.
    descripcion: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
    preciop: /^\d{1,20}$/, // 7 a 14 numeros.	
}

const campos = {
	id : false, 
	nombre : false,
	stock : false,
	descripcion : false,
    preciop : false,
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "id":
			validarCampo(expresiones.id, e.target, 'id');
		break;

		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;

		case "stock":
			validarCampo(expresiones.stock, e.target, 'stock');
		break;

		case "descripcion":
			validarCampo(expresiones.descripcion, e.target, 'descripcion')
		break;

        case "preciop":
			validarCampo(expresiones.preciop, e.target, 'preciop')
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

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario)
});


formRegistro.addEventListener('submit', (e) => {

	
	if(campos.id && campos.nombre && campos.stock && campos.descripcion && campos.preciop != false){
		

	} else {
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
		setTimeout(() => {
			//cuando pasen 5 segundos el mensaje se eliminara
			document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
		}, 5000)
		e.preventDefault();
	}

})