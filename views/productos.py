from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedProductoSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
from django.db.models import Q
from api_factura.models import Producto

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from PIL import Image
from base64 import decodestring,decodebytes
from json import loads
#import StringIO
import base64
from io import StringIO,BytesIO
import io
from api.settings import MEDIA_ROOT,MEDIA_URL
import os

@api_view(['GET', 'POST'])
def producto_listado(request):
    #from api_pollo.models import Personal
    #Codigo de verificacion de asignacion de modulo    
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[8]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    #print(modulo_valido)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    #print(bd)
    # termina verificaciond e modulo
    if request.method=='GET':
        #print(request.QUERY_PARAMS)
        if request.QUERY_PARAMS.get('param') is not None:
            
            param=request.QUERY_PARAMS.get('param')
            productos = Producto.objects.using(bd).filter(Q(estado=True),
                                                        Q(nombre__icontains = param) |
                                                        Q(descripcion__icontains=param))            
        else:
            productos = Producto.objects.using(bd).filter(estado=True)
        #print(len(personal))
        paginator = Paginator(productos, 10)
        
        page = request.QUERY_PARAMS.get('page')
        try:
            registros = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            registros = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            registros = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        #print(registros)
        serializer = PaginatedProductoSerializer(registros,
                                             context=serializer_context)
        return Response(serializer.data)
    
    elif request.method=='POST':
        fecha=datetime.now().strftime("%Y-%m-%d")
        data={}
        for dato in request.DATA:
            if request.DATA[dato]!='' and dato!='img_150x150' and dato!='img_500x500':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        producto=Producto(nombre=data['nombre'],
                        descripcion=data['descripcion'],
                        fecha=fecha,
                        estado=True)
        
        producto.save(using=bd)
        ruta_150x150=''
        ruta_500x500=''
        if request.DATA['img_150x150']!=None and request.DATA['img_500x500']!=None:
            photo1 = request.DATA['img_150x150'].partition('base64,')[2]
            image_150x150 = base64.b64decode(photo1)
            photo2 = request.DATA['img_500x500'].partition('base64,')[2]
            image_500x500 = base64.b64decode(photo2)
            
            ruta=str(user.empresa.id)+'/productos/'+str(producto.id)
            fecha_img=datetime.now().strftime("%Y%m%d%H%M%S")
            ruta_150x150=ruta+'/'+fecha_img+'_principal_150x150.jpeg'#+request.DATA['img_nombre']
            ruta_500x500=ruta+'/'+fecha_img+'_principal_500x500.jpeg'#+request.DATA['img_nombre']
            ruta_=MEDIA_ROOT+'/'+ruta
            if not os.path.exists(ruta_): os.makedirs(ruta_)
            ruta1_full=MEDIA_ROOT+ruta_150x150
            ruta2_full=MEDIA_ROOT+ruta_500x500
            
            image = Image.open(io.BytesIO(image_150x150))
            image.save(ruta1_full)
            image = Image.open(io.BytesIO(image_500x500))
            image.save(ruta2_full)
            
            producto.img=ruta
            producto.img_date=fecha_img
            producto.save(using=bd)
            ruta_150x150=MEDIA_URL+ruta_150x150
            ruta_500x500=MEDIA_URL+ruta_500x500
        respuesta={"id":producto.id,"img_150x150":ruta_150x150,"img_500x500":ruta_500x500}
        
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def producto_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if Producto.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        producto=Producto.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='' and dato!='img_150x150' and dato!='img_500x500':
                data[dato]=request.DATA[dato]                 
            else:
                data[dato]=None        
        
        producto.nombre=data['nombre']
        producto.descripcion=data['descripcion']
        #print(data)
        ruta_150x150=''
        ruta_500x500=''
        img_cambio=False
        ruta=str(user.empresa.id)+'/productos/'+str(producto.id)
        if request.DATA['img_150x150']!=None and request.DATA['img_500x500']!=None:
            photo1 = request.DATA['img_150x150'].partition('base64,')[2]
            image_150x150 = base64.b64decode(photo1)
            photo2 = request.DATA['img_500x500'].partition('base64,')[2]
            image_500x500 = base64.b64decode(photo2)
            fecha_img=datetime.now().strftime("%Y%m%d%H%M%S")
            
            ruta_150x150=ruta+'/'+fecha_img+'_principal_150x150.jpeg'#+request.DATA['img_nombre']
            ruta_500x500=ruta+'/'+fecha_img+'_principal_500x500.jpeg'#+request.DATA['img_nombre']
            ruta_=MEDIA_ROOT+'/'+ruta
            
            if producto.img_date!=None and producto.img_date!='':
                img_anterior150=MEDIA_ROOT+'/'+ruta+'/'+producto.img_date+'_principal_150x150.jpeg'
                if os.path.isfile(img_anterior150) and os.access(img_anterior150, os.R_OK):
                    os.remove(img_anterior150)
                img_anterior500=MEDIA_ROOT+'/'+ruta+'/'+producto.img_date+'_principal_500x500.jpeg'
                if os.path.isfile(img_anterior500) and os.access(img_anterior500, os.R_OK):
                    os.remove(img_anterior500)
            
            if not os.path.exists(ruta_): os.makedirs(ruta_)
            ruta1_full=MEDIA_ROOT+ruta_150x150
            ruta2_full=MEDIA_ROOT+ruta_500x500
            
            image = Image.open(io.BytesIO(image_150x150))
            image.save(ruta1_full)
            image = Image.open(io.BytesIO(image_500x500))
            image.save(ruta2_full)
            
            producto.img=ruta
            producto.img_date=fecha_img
            ruta_150x150=MEDIA_URL+ruta_150x150
            ruta_500x500=MEDIA_URL+ruta_500x500            
        elif request.DATA.get('eliminar')==True:
            img_anterior150=MEDIA_ROOT+'/'+ruta+'/'+producto.img_date+'_principal_150x150.jpeg'
            if os.path.isfile(img_anterior150) and os.access(img_anterior150, os.R_OK):
                os.remove(img_anterior150)
            img_anterior500=MEDIA_ROOT+'/'+ruta+'/'+producto.img_date+'_principal_500x500.jpeg'
            if os.path.isfile(img_anterior500) and os.access(img_anterior500, os.R_OK):
                os.remove(img_anterior500)
            producto.img=None
            producto.img_date=None
        #print(img_cambio)
        if producto.has_changed==True:
            producto.save(using=bd)
            respuesta={"respuesta":1,"img_150x150":ruta_150x150,"img_500x500":ruta_500x500}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            if producto.img_date!=None and producto.img_date!='':
                ruta_150x150=MEDIA_URL+'/'+ruta+'/'+producto.img_date+'_principal_150x150.jpeg'
                ruta_500x500=MEDIA_URL+'/'+ruta+'/'+producto.img_date+'_principal_500x500.jpeg'
                
            respuesta={"respuesta":2,"img_150x150":ruta_150x150,"img_500x500":ruta_500x500}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if Producto.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        producto=Producto.objects.using(bd).get(id=pk)
        producto.estado=False
        producto.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)
