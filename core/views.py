from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Tipo, Producto, Usuario, Comuna, Direccion, Region, Pregunta, Rol, Producto, DetallePedido, Pedido
from django.contrib import messages                                 # MENSAJES
from django.http import JsonResponse
from django.contrib.auth.models import User
from .context_processor import total_carrito
import flow_api.views as flow
from datetime import date

from .carrito import Carrito


# Create your views here.
def zinicio(request):
    return render(request, 'core/zinicio.html')


@login_required
def mostrarmenuuser(request):
    productos = Producto.objects.all()
    contexto = {
        "listaProductos": productos
    }
    return render(request, 'core/MainMenuUser.html', contexto)

@login_required
def botonModificar(request, idP):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        producto = Producto.objects.get(idProducto = idP)
        contexto = {
            "dato": producto
        }
        return render(request, 'core/editcomacana.html', contexto)
    else:
        return render(request, 'core/paginaError.html')

@login_required
def actualizarProducto(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        idP = request.POST['idProducto']
        producto = Producto.objects.get(idProducto = idP)
        nombrep = request.POST['nombrep']
        preciop = request.POST['preciop']
        descp = request.POST['descp']
        stockp = request.POST['stockp']
        if request.FILES.get('fotoNueva'):
            producto.foto = request.FILES.get('fotoNueva')
        else:
            producto.foto = producto.foto

        producto.nombreProducto = nombrep
        producto.precio = preciop
        producto.descripcionProducto = descp
        producto.stock = stockp
        
        producto.save()
        messages.success(request, "Producto modificado Exitosamente!")
        return redirect('mostrareliminarproducto')
    else:
        return render(request, 'core/paginaError.html')
        
    
@login_required
def mostrareliminarproducto(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        # productos = Producto.objects.all()
        
        # Obtener el término de búsqueda de la URL
        # request.GET.get -> El primer GET es para que obtenga los datos, el segundo get es solamente el nombre
        # 
        query = request.GET.get('NombreProducto', '')
        
        if query:
            # Filtrar productos por el término de búsqueda
            # nombreProducto__icontains = Esto es para que tome las palabras mayusculas y minusculas
            productos = Producto.objects.filter(nombreProducto__icontains=query)
            # productos = Producto.objects.filter(idProducto__icontains=query)
        else:
            # Si no hay término de búsqueda, mostrar todos los productos
            productos = Producto.objects.all()

        contexto = {
            "listaProductos": productos
        }
        return render(request, 'core/eliminarproducto.html', contexto)
    else:
        return render(request, 'core/paginaError.html')
    
@login_required
def botoneliminar(request, idP):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        productos = Producto.objects.get(idProducto = idP)
        productos.delete()
        messages.success(request, "Producto Eliminado Exitosamente")
        return redirect('mostrareliminarproducto')
    else:
        return render(request, 'core/paginaError.html')
    


def MainMenu(request):
    # Obtener el término de búsqueda de la URL
    # request.GET.get -> El primer GET es para que obtenga los datos, el segundo get es solamente el nombre
    # 
    query = request.GET.get('NombreProducto', '')
    
    if query:
        # Filtrar productos por el término de búsqueda
        # nombreProducto__icontains = Esto es para que tome las palabras mayusculas y minusculas
        productos = Producto.objects.filter(nombreProducto__icontains=query)
    else:
        # Si no hay término de búsqueda, mostrar todos los productos
        productos = Producto.objects.all()

    contexto = {
        "listaProductos": productos
    }
    return render(request, 'core/MainMenu.html', contexto)

#carga de datos
def botonMostrar(request, idP):
    producto = Producto.objects.get(idProducto = idP)
    contexto = {
        "dato": producto
    }
    return render(request, 'core/jugbolasi.html', contexto)

# carga los datos de productos especificos cuando se selecciona en el menu principal
def mostrarjuguetebolasi(request):
    return render(request,'core/jugbolasi.html')                                        #Fin menu principal usuario

                                                    
                                                                            

def carrito(request):                                                                   # Inicio  carrito
    ctx={
        "rs":Region.objects.all(),
        "cs":Comuna.objects.all(),
    }
    return render(request, 'core/carrito.html',ctx)

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.agregar(producto)
    return redirect('carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.restar(producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('carrito')                                                              # Final   carrito
                                                                       
#carrito de compra usuario resta de stock
@login_required
def comprar(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        region = request.POST.get('region')
        comuna = request.POST.get('comuna')
        address = request.POST.get('adress')
        postal_code = request.POST.get('postalcode')
        
        # Actualizar el stock de los productos en la base de datos
        carrito = request.session.get('carrito')
        if carrito:
            #DBregion = Region.objects.get(codigoRegion = region)
            DBcomuna = Comuna.objects.get(codigoComuna = comuna)
            DBuser = Usuario.objects.get(correo = request.user.email)
            newDireccion = Direccion.objects.create(nombreCalle = address, codigoPostal = postal_code, idUsuario = DBuser, comuna = DBcomuna)
            newPedido = Pedido.objects.create(fechaPedido = date.today(), fechaEntrega = date.today(), estado = "Pagado", total = total_carrito(request)["total_carrito"], idDireccion = newDireccion, usuario = DBuser)
            if not newPedido:
                messages.error(request, f"No se pudo crear el pedido")
                return redirect('carrito')
            for producto_id, item in carrito.items():
                producto = Producto.objects.get(idProducto=producto_id)
                cantidad_comprada = item['cantidad']
                if producto.stock >= cantidad_comprada:
                    producto.stock -= cantidad_comprada
                    producto.save()
                    newDetalle = DetallePedido.objects.create(cantidad = cantidad_comprada, subtotal = producto.precio * cantidad_comprada, pedido = newPedido, producto = producto)
                else:
                    messages.error(request, f"No hay suficiente stock para el producto {producto.nombreProducto}. Stock del producto: {producto.stock}")
                    return redirect('carrito')
            pay_commerceOrder = newPedido.idPedido
            pay_subject = "Compra Productos Mascotas ToshivePet"
            pay_amount = total_carrito(request)["total_carrito"]
            pay_email = DBuser.correo
            pay_urlConfirmation = "https://feigonzalez.wordpress.com"
            pay_urlReturn = "http://localhost:8000/paginacompralista/"
            
            carritolim = Carrito(request)
            carritolim.limpiar()
            
            print("\n  [>] Creating Payment")
            print("commerceOrder  :",pay_commerceOrder)
            print("subject        :",pay_subject)
            print("amount         :",pay_amount)
            print("email          :",pay_email)
            print("urlConfirmation:",pay_urlConfirmation)
            print("urlReturn      :",pay_urlReturn)
            fResponse = flow.createPayment(pay_commerceOrder, pay_subject, pay_amount, pay_email, pay_urlConfirmation, pay_urlReturn)
            print(fResponse)
            if "code" in fResponse:
                print("\n  [!] Error in request to Flow\n")
                messages.error(request, flow.clientifyErrorMessage(fResponse))
                return render(request, 'core/carrito.html')
            return redirect(fResponse["url"]+"?token="+fResponse["token"])
        else:
            print("\n  [!] 'carrito' not defined. Could be caused because it's empty\n")
    return redirect('carrito')

@login_required
def seguimiento(request):
    return render(request, 'core/seguimiento.html')

@csrf_exempt
def compralista(request):
    return render(request, 'core/compralista.html')

#PERFIL USUARIO CARGA DE DATOS
@login_required
def PerfilUser(request):
    # Obtener el usuario actualmente autenticado
    usuario = request.user
    usuarioT = Usuario.objects.get(correo = usuario.email)
    # Pasar los datos del usuario al contexto
    contexto = {
        'usuario': usuario,
        "usuarioT":usuarioT
        }
    return render(request, 'core/PerfilUser.html', contexto)

@login_required
def cambiosPerfil(request):
    # el nombre que reciben los post es el name=x que tiene la etiqueta del html
    usuarioId = request.POST['idUsuario']
    usuarioCambio = Usuario.objects.get(idUsuario = usuarioId)
    nombreUsuario = request.POST['nombre']
    nombreCorreo = request.POST['emailCorreo']
    clavePrivada = request.POST['pass']
    telefono = request.POST['phone']

    usuarioCambio.nombreUsuario = nombreUsuario
    usuarioCambio.telefono = telefono
    usuarioCambio.clave = clavePrivada
    u = User.objects.get(username=nombreCorreo)
    u.set_password(clavePrivada)
    u.save()

    usuarioCambio.save()
    messages.success(request, "Usuario Actualizado")
    return redirect('mostrarmenuuser')
                                                                                                                     #ADMINISTRADOR
@login_required                                                                                                 
def listarUsuarios(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        usuarios = Usuario.objects.all()
        contexto = {
            "listUsers":usuarios
        }
        return render(request, 'core/listarUsuarios.html',contexto)
    else:
        return render(request, 'core/paginaError.html')
    
@login_required
def cargaInfoUsuario(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        return render (request, 'core/infoUsuario.html')
    else:
        return render(request, 'core/paginaError.html')

@login_required
def cambiarStatus(request, idU):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        userid = Usuario.objects.get(idUsuario = idU)
        tipo = Rol.objects.all()
        contexto = {
            "datoUsuario": userid,
            "listaTipos": tipo
        }
        return render(request, 'core/infoUsuario.html', contexto)
    else:
        return render(request, 'core/paginaError.html')

@login_required
def actualizarUsuario(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        idU = request.POST['idUsuario']
        UsuarioInfo = Usuario.objects.get(idUsuario = idU)
        nombrep = request.POST['nombreUsuario']
        correo = request.POST['correo']
        status = request.POST['nombreRol']

        UsuarioInfo.nombreUsuario = nombrep
        UsuarioInfo.correo = correo
        registroStatus = Rol.objects.get(nombreRol = status)
        UsuarioInfo.idRol = registroStatus

        UsuarioInfo.save()
        messages.success(request, "Usuario modificado Exitosamente!")
        return redirect('listarUsuarios')
    else:
        return render(request, 'core/paginaError.html')

#LISTADO DE API EN PERFIL USUARIO
@login_required
def Listado_API(request): 
    return render(request, 'core/Listado_API.html')

                        
def registroAlternativo(request):               #vista para obtener los datos del formulario registro
    preguntas = Pregunta.objects.all()
    contexto = {
        "listaPreguntas": preguntas
    }
    return render(request,'core/registroAlternativo.html', contexto)                                                                             

def registroAlternativoG(request):
    nombreU = request.POST['nombre']
    emailU = request.POST['correo']
    if User.objects.filter(email=emailU).exists():
        messages.error(request, f"El email: {emailU} ya existe")
        return render(request, 'core/zinicio.html')
    telefonoU = request.POST['telefono']
    passW = request.POST['password']
    preguntaU = request.POST['pregunta']
    respuestaU = request.POST['respuesta']
    
    registroPregunta = Pregunta.objects.get(idPregunta = preguntaU)
    registroIdrol = Rol.objects.get(idRol=2)
    user = Usuario.objects.create(nombreUsuario = nombreU, correo = emailU, telefono = telefonoU, clave = passW, respuesta = respuestaU, idPregunta = registroPregunta, idRol = registroIdrol)
    print("User created on site database")
    fResponse = flow.createCustomer(user.nombreUsuario, user.correo, user.idUsuario)
    print(fResponse)
    if "code" in fResponse:
        print("ERROR on flow.createCustomer:")
        user.delete()
        messages.error(request,flow.clientifyErrorMessage(fResponse))
    else:
        print("User created on flow")
        djuser = User.objects.create_user(username=emailU, email=emailU, password=passW, last_name = respuestaU)
        messages.success(request, "Usuario creado Exitosamente!")
        djuser.is_staff=False
        djuser.is_active=True
        djuser.save()
        print("User created on django database")
    return redirect('zinicio')

def iniciar_sesion(request):
    usuario1 = request.POST['formCorreo']
    contra1 = request.POST['formClave']
    try:   
        user1 = User.objects.get(username = usuario1)
    except User.DoesNotExist:
        messages.error(request,'El usuario o contraseña son incorrectos')
        return redirect('zinicio')

    pass_valida = check_password(contra1, user1.password)
    if not pass_valida:
        messages.error(request, 'El usuario o contraseña son incorrectos ')
        return redirect('zinicio')
    usuario2 = Usuario.objects.get(correo = usuario1, clave = contra1)
    user = authenticate(username=usuario1, password=contra1)
    if user is not None:
        login(request,user)
        if (usuario2.idRol.nombreRol == 'Administrador'):
            user.is_superuser = True
            user.save()
            return redirect('listarUsuarios')
        else:
            user.is_superuser = False
            user.save()
            
            return redirect('mostrarmenuuser')
    else:
        return render(request, 'core/zinicio.html')
    
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('zinicio')
                                                                            
def contraAlternativo(request):                                                             #Recuperar contraseña
    return render(request, 'core/contraAlternativo.html')

def recuperarContra(request):
    usuarioUno = request.POST['emailRecuperativo']
    contraUno = request.POST['passwordRecuperativo']
    try:   
        user1 = User.objects.get(username = usuarioUno)
    except User.DoesNotExist:
        messages.error(request,'El usuario o respuesta son incorrectos')
        return redirect('zinicio')

    if contraUno != user1.last_name:
        messages.error(request, 'El usuario o respuesta son incorrectos')
        return redirect('zinicio')
    usuario2 = Usuario.objects.get(correo = usuarioUno, respuesta = contraUno)
    if user1.username == usuarioUno and user1.last_name == contraUno:
        login(request,user1)
        if (usuario2.idRol.nombreRol == 'Administrador'):
            user1.is_superuser = True
            user1.save()
            return redirect('listarUsuarios')
        else:
            user1.is_superuser = False
            user1.save()

            return redirect('mostrarmenuuser')
    else:
        return render(request, 'core/zinicio.html')
    
#admin
@login_required
def editcomacana(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        return render(request, 'core/editcomacana.html')
    else:
        return render(request, 'core/paginaError.html')

#admin
@login_required
def ingresarproductos(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        tipo = Tipo.objects.all()
        contexto = {
            "listaTipos": tipo
        }
        return render(request, 'core/ingresarproductos.html', contexto)
    else:
        return render(request, 'core/paginaError.html')

#   Vista para obtener datos del formulario ingresarProductos   ADMIN
@login_required
def insertarProductost(request):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        idP = request.POST['id']
        tipoP = request.POST['tipo']
        nombreP = request.POST['nombre']
        stockP = request.POST['stock']            
        fotoP = request.FILES['fotop']
        descripcionP = request.POST['descripcion']
        precioP = request.POST['preciop']        

        registroTipo = Tipo.objects.get(idTipo = tipoP)
        
        if Producto.objects.filter(idProducto=idP).exists():
            messages.warning(request, f"El id: {idP} ya existe")
            return redirect('ingresarproductos')
        else:
            
            Producto.objects.create(idProducto = idP, nombreProducto = nombreP, descripcionProducto = descripcionP, stock = stockP, precio = precioP, foto = fotoP, tipo = registroTipo)
            
            messages.success(request, "Producto ingresado Exitosamente!")
            return redirect('ingresarproductos')
            #return redirect('mostrareliminarproducto')
    else:
        return render(request, 'core/paginaError.html')
    
#def botoneliminar(request, idP):
    if request.user.is_superuser or (isinstance(request.user, Usuario) and request.user.idRol.nombreRol == "Administrador"):
        productos = Producto.objects.get(idProducto = idP)
        productos.delete()
        messages.success(request, "Producto Eliminado Exitosamente")
        return redirect('mostrareliminarproducto')
    else:
        return render(request, 'core/paginaError.html')





