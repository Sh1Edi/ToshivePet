from rest_framework import serializers
from core.models import Comuna, Direccion   # 2 tablas con almenos 3 datos (claves foraneas igual cuentan)
# las tablas no deben contener ninguna foto
class ComunaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields=['codigoComuna','nombreComuna','region']# se recomienda tener el mismo orden de la tabla para evitar errores

class DireccionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields=['idDireccion','nombreCalle','idUsuario','comuna']