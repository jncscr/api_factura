from api_factura.models import Producto,Caracteristica
#from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import pagination
#from datetime import datetime
#from django.db.models import Q
#from django.db import connections

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id','nombre','descripcion')  
        
class CaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ('id','nombre','estado')  
        
class PaginatedProductoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoSerializer

class PaginatedCaracteristicaSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=CaracteristicaSerializer
