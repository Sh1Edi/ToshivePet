from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Comuna, Direccion
from .serializers import ComunaSerializers, DireccionSerializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
@csrf_exempt
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def lista_comunas(request):
    """
    lista de todas las comunas
    """
    if request.method == 'GET':
        comuna = Comuna.objects.all()
        serializer = ComunaSerializers(comuna, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ComunaSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def lista_direccion(request):
    """
    lista de todas las Direcciones
    """
    if request.method == 'GET':
        direccion = Direccion.objects.all()
        serializer = DireccionSerializers(direccion, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DireccionSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view (['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def detalle_comunas(request, id):
    
    try:
        comuna = Comuna.objects.get(codigoComuna = id)
    except Comuna.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ComunaSerializers(comuna, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        comuna.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view (['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def detalle_direccion(request, id):
    
    try:
        direccion = Direccion.objects.get(idDireccion = id)
    except Direccion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DireccionSerializers(direccion, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        direccion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

