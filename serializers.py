from api_factura.models import Producto
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
        
class PaginatedProductoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoSerializer

