from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from.views import cambiosPerfil,recuperarContra,actualizarUsuario,cargaInfoUsuario,cambiarStatus,cerrar_sesion,iniciar_sesion,zinicio,listarUsuarios,comprar, limpiar_carrito,restar_producto,eliminar_producto,agregar_producto,compralista, registroAlternativoG, botonMostrar,actualizarProducto, botonModificar, botoneliminar, insertarProductost, mostrarmenuuser, mostrareliminarproducto, mostrarjuguetebolasi, MainMenu, carrito, seguimiento,registroAlternativo, PerfilUser, Listado_API, ingresarproductos, editcomacana, contraAlternativo

urlpatterns = [
    path('', MainMenu, name="MainMenu"),
    path('paginamostrarmenuuser/',mostrarmenuuser,name="mostrarmenuuser"),
    path('paginaeliminarproducto/',mostrareliminarproducto,name="mostrareliminarproducto"),
    path('paginajuguetebolasi/',mostrarjuguetebolasi,name="mostrarjuguetebolasi"),
    path('paginacarrito/', carrito, name="carrito"),
    path('paginaseguimiento/', seguimiento , name="seguimiento"),
    path('paginacompralista/', compralista , name="compralista"),
    path('paginaregistroAlternativo/', registroAlternativo , name="registroAlternativo"),
    path('paginaPerfilUser/', PerfilUser , name="PerfilUser"),
    path('paginaListado_API/', Listado_API , name="Listado_API"),
    path('paginaingresarproductos/', ingresarproductos , name="ingresarproductos"),
    path('paginaeditcomacana/', editcomacana , name="editcomacana"),
    path('paginacontraAlternativo/', contraAlternativo , name="contraAlternativo"),
    path('insertarProductost/', insertarProductost , name="insertarProductost"),
    path('botoneliminar/<int:idP>', botoneliminar, name="botoneliminar"),
    path('botonModificar/<int:idP>', botonModificar, name="botonModificar"),
    path('actualizarProducto/', actualizarProducto, name="actualizarProducto"),
    path('botonMostrar/<int:idP>',botonMostrar,name="botonMostrar"),
    path('registroAlternativoG', registroAlternativoG , name="registroAlternativoG"),
    path('agregar/<int:producto_id>/',agregar_producto, name="agregar"),
    path('eliminar/<int:producto_id>/',eliminar_producto,name="eliminar"),
    path('restar/<int:producto_id>/',restar_producto,name="restar"),
    path('limpiar/',limpiar_carrito,name="limpiar"),
    path('comprar/', views.comprar, name='comprar'),
    path('listarUsuarios/', listarUsuarios, name="listarUsuarios"),
    path('accounts/login/',zinicio,name="zinicio"),
    path('iniciar_sesion/',iniciar_sesion,name="iniciar_sesion"),
    path('cerrar_sesion/',cerrar_sesion,name="cerrar_sesion"),
    path('cambiarStatus/<int:idU>', cambiarStatus, name="cambiarStatus"),
    path('cargaInfoUsuario/', cargaInfoUsuario, name="cargaInfoUsuario"),
    path('actualizarUsuario/', actualizarUsuario, name="actualizarUsuario"),
    path('recuperarContra/',recuperarContra,name="recuperarContra"),
    path('cambiosPerfil/',cambiosPerfil,name="cambiosPerfil"),

]

