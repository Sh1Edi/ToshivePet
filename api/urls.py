from django.urls import path
from .views import lista_comunas, lista_direccion, detalle_comunas,detalle_direccion
from .viewsLogin import login

urlpatterns=[
    path('lista_comunas', lista_comunas, name="lista_comunas"),
    path('lista_direccion', lista_direccion, name="lista_direccion"),
    path('detalle_comunas/<id>',detalle_comunas, name="detalle_comunas"),
    path('detalle_direccion/<id>',detalle_direccion,name="detalle_direccion"),
    path('login', login, name="login"),
]