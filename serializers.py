from api_factura.models import Producto,Caracteristica,Atributo,TipoControl
from api_factura.models import AtributoValor,ProductoCaracteristica,ProductoAtributo
from api_factura.models import Personal
#from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import pagination
#from datetime import datetime
#from django.db.models import Q
#from django.db import connections
from api.settings import MEDIA_URL

class ProductoSerializer(serializers.ModelSerializer):
    img_150x150 = serializers.SerializerMethodField('get_img_150x150')
    img_500x500 = serializers.SerializerMethodField('get_img_500x500')
    class Meta:
        model = Producto
        fields = ('id','nombre','descripcion','img_150x150',
                    'img_500x500')  
    def get_img_150x150(self,obj):
        if obj.img!=None and obj.img!='':
            return MEDIA_URL+obj.img+'/'+obj.img_date+'_principal_150x150.jpeg'
        else:
            return None
    def get_img_500x500(self,obj):
        if obj.img!=None and obj.img!='':
            return MEDIA_URL+obj.img+'/'+obj.img_date+'_principal_500x500.jpeg'
        else:
            return None
class CaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ('id','nombre','estado')  

class ProductoCaracteristicaSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField('get_nombre')
    class Meta:
        model = ProductoCaracteristica
        fields = ('id','valor','estado','caracteristica',
                'nombre')
    def get_nombre(self, obj):
        
        return obj.caracteristica.nombre
    
class AtributoSerializer(serializers.ModelSerializer):
    tipo_control_lb = serializers.SerializerMethodField('get_tipo_control_lb')
    class Meta:
        model = Atributo
        fields = ('id','nombre','estado','tipo_control','tipo_control_lb')  
    def get_tipo_control_lb(self, obj):
        return obj.tipo_control.nombre

class ProductoAtributoSerializer(serializers.ModelSerializer):
    tipo_control_lb = serializers.SerializerMethodField('get_tipo_control_lb')
    atributo_lb = serializers.SerializerMethodField('get_atributo_lb')
    class Meta:
        model = ProductoAtributo
        fields = ('id','estado','tipo_control','tipo_control_lb',
                'atributo','atributo_lb')  
    def get_tipo_control_lb(self, obj):
        return obj.tipo_control.nombre
    def get_atributo_lb(self, obj):
        return obj.atributo.nombre
    
class AtributoValorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoValor
        fields = ('id','valor','atributo','estado')  

class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ('id','nombres','apellidos',
                'telefono','direccion','empresa',
                'nit')

class PaginatedProductoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoSerializer

class PaginatedCaracteristicaSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=CaracteristicaSerializer

class PaginatedProductoCaracteristicaSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoCaracteristicaSerializer

class PaginatedAtributoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=AtributoSerializer

class PaginatedAtributoValorSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=AtributoValorSerializer

class PaginatedProductoAtributoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoAtributoSerializer

class PaginatedPersonalSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=PersonalSerializer