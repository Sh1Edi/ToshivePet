from django.db import models

# Create your models here.
class Tipo(models.Model):
    idTipo = models.AutoField(primary_key=True,verbose_name='Id tipo')
    descripcion = models.CharField(max_length=40)
    def __str__(self) -> str:
        return self.descripcion

class Producto(models.Model):
    idProducto = models.IntegerField(primary_key=True)
    nombreProducto = models.CharField(max_length=300)
    descripcionProducto = models.CharField(max_length=500)
    stock = models.IntegerField()
    precio = models.IntegerField()
    foto = models.ImageField(upload_to="toshibedjango")
    #claves foraneas
    tipo = models.ForeignKey(Tipo,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.nombreProducto

    # independiente
class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombreRol = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.nombreRol

class Region(models.Model):
    codigoRegion = models.AutoField(primary_key=True,verbose_name='Codigo de Region')
    nombreRegion = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.nombreRegion   
    
class Comuna(models.Model):
    codigoComuna = models.AutoField(primary_key=True)
    nombreComuna = models.CharField(max_length=30)
    #claves foraneas
    region = models.ForeignKey(Region,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.nombreComuna


class Pregunta(models.Model):
    idPregunta = models.AutoField(primary_key=True, verbose_name='Id Pregunta')
    pregunta = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.pregunta

    # dependiente 
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=50)
    correo = models.CharField(max_length=40)
    telefono = models.CharField(max_length=20)
    clave = models.CharField(max_length=20)
    respuesta = models.CharField(max_length=20)
    #claves foraneas
    idPregunta = models.ForeignKey(Pregunta,on_delete=models.DO_NOTHING)
    idRol = models.ForeignKey(Rol,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:   
        return self.nombreUsuario

class Direccion(models.Model):
    idDireccion = models.AutoField(primary_key=True)
    nombreCalle = models.CharField(max_length=30)
    codigoPostal = models.CharField(max_length=40)
    #claves foraneas
    idUsuario = models.ForeignKey(Usuario,on_delete=models.DO_NOTHING)
    comuna = models.ForeignKey(Comuna,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.nombreCalle


class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True, verbose_name='ID de Pedido')
    fechaPedido = models.DateTimeField(verbose_name='Fecha de Pedido')
    fechaEntrega = models.DateTimeField(verbose_name='Fecha de Entrega')
    estado = models.CharField(max_length=50, verbose_name='Estado')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    #claves foraneas
    idDireccion = models.ForeignKey(Direccion, on_delete=models.DO_NOTHING, verbose_name='ID de Dirección')
    usuario = models.ForeignKey(Usuario,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.estado

class DetallePedido(models.Model):
    idDetalle = models.AutoField(primary_key=True, verbose_name='ID de Detalle')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Subtotal')
    #claves foraneas
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, verbose_name='ID de Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, verbose_name='ID de Producto')
   