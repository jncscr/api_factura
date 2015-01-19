from api_factura.models import Producto,Caracteristica,Atributo,TipoControl,AtributoValor
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

class AtributoSerializer(serializers.ModelSerializer):
    tipo_control_lb = serializers.SerializerMethodField('get_tipo_control_lb')
    class Meta:
        model = Atributo
        fields = ('id','nombre','estado','tipo_control','tipo_control_lb')  
    def get_tipo_control_lb(self, obj):
        control=TipoControl.objects.using(obj._state.db).get(id=obj.tipo_control.id)
        return control.nombre

class AtributoValorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoValor
        fields = ('id','valor','atributo','estado')  
        
class PaginatedProductoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=ProductoSerializer

class PaginatedCaracteristicaSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=CaracteristicaSerializer

class PaginatedAtributoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=AtributoSerializer

class PaginatedAtributoValorSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class=AtributoValorSerializer