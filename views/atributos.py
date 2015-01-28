from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedAtributoSerializer,PaginatedAtributoValorSerializer
from api_factura.serializers import PaginatedProductoAtributoSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
from django.db.models import Q
from api_factura.models import Atributo,AtributoValor,ProductoAtributo

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import connections

@api_view(['GET', 'POST'])
def atributo_listado(request):
    #from api_pollo.models import Personal
    #Codigo de verificacion de asignacion de modulo    
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    #print(modulo_valido)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    #print(bd)
    # termina verificaciond e modulo
    if request.method=='GET':
        if request.QUERY_PARAMS.get('param') is not None:
            
            param=request.QUERY_PARAMS.get('param')
            atributos = Atributo.objects.using(bd).filter(Q(estado=True),
                                                        Q(id__icontains = param)|
                                                        Q(nombre__icontains = param)|
                                                        Q(tipo_control__nombre__icontains=param))            
        else:
            atributos = Atributo.objects.using(bd).filter(estado=True)
        #print(len(personal))
        numPages=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(atributos,numPages)
        
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
        serializer = PaginatedAtributoSerializer(registros,
                                             context=serializer_context)
        
        return Response(serializer.data)
    
    elif request.method=='POST':
        data={}        
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='tipo_control':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]
            else:
                data[dato]=None        
        atributo=Atributo(nombre=data['nombre'],
                        estado=True,
                        tipo_control_id=data['tipo_control'])        
        atributo.save(using=bd)
        respuesta={"id":atributo.id,'tipo_control_lb':atributo.tipo_control.nombre}
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def atributo_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if Atributo.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=Atributo.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='tipo_control':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]                 
            else:
                data[dato]=None        
        
        atributo.nombre=data['nombre']
        atributo.tipo_control_id=data['tipo_control']
        #print(data)
        if atributo.has_changed==True:
            atributo.save(using=bd)
            respuesta={"respuesta":1,'tipo_control_lb':atributo.tipo_control.nombre}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if Atributo.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=Atributo.objects.using(bd).get(id=pk)
        atributo.estado=False
        atributo.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def atributo_val_listado(request):
    #from api_pollo.models import Personal
    #Codigo de verificacion de asignacion de modulo    
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    #print(modulo_valido)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    #print(bd)
    # termina verificaciond e modulo
    if request.method=='GET':
        id_atr=request.QUERY_PARAMS.get('id_atr')
        if request.QUERY_PARAMS.get('param') is not None:
            
            param=request.QUERY_PARAMS.get('param')
            atributos = AtributoValor.objects.using(bd).filter(Q(estado=True),
                                                        Q(atributo_id=id_atr),
                                                        Q(id__icontains = param)|
                                                        Q(valor__icontains=param))            
        else:
            atributos = AtributoValor.objects.using(bd).filter(estado=True,atributo_id=id_atr)
        #print(len(personal))
        numPages=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(atributos,numPages)
        
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
        serializer = PaginatedAtributoValorSerializer(registros,
                                             context=serializer_context)
        
        return Response(serializer.data)
    
    elif request.method=='POST':
        data={}        
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='atributo':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]
            else:
                data[dato]=None        
        atributo=AtributoValor(valor=data['valor'],
                        estado=True,
                        atributo_id=data['atributo'])        
        atributo.save(using=bd)
        respuesta={"id":atributo.id,'atributo':atributo.id}
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def atributo_val_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if AtributoValor.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=AtributoValor.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]                 
            else:
                data[dato]=None        
        
        atributo.valor=data['valor']
        #print(data)
        if atributo.has_changed==True:
            atributo.save(using=bd)
            respuesta={"respuesta":1}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if AtributoValor.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=AtributoValor.objects.using(bd).get(id=pk)
        atributo.estado=False
        atributo.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def atributo_producto_listado(request):
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
        id_prod=request.QUERY_PARAMS.get('id')
        if request.QUERY_PARAMS.get('param') is not None:            
            param=request.QUERY_PARAMS.get('param')
            atributos = ProductoAtributo.objects.using(bd).filter(Q(estado=True),
                                                        Q(atributo__estado=True),
                                                        Q(producto_id=id_prod),
                                                        Q(id__icontains = param)|
                                                        Q(atributo__nombre__icontains = param)|
                                                        Q(tipo_control__nombre__icontains=param))            
        else:
            atributos = ProductoAtributo.objects.using(bd).filter(estado=True,
                                                        atributo__estado=True,
                                                        producto_id=id_prod)
        #print(len(personal))
        numPages=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(atributos,numPages)
        
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
        serializer = PaginatedProductoAtributoSerializer(registros,
                                             context=serializer_context)
        
        return Response(serializer.data)
    
    elif request.method=='POST':
        data={}        
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]
            else:
                data[dato]=None        
        atributo=ProductoAtributo(atributo_id=data['atributo'],
                        estado=True,
                        tipo_control_id=data['tipo_control'],
                        producto_id=data['producto'])        
        atributo.save(using=bd)
        respuesta={"id":atributo.id,'tipo_control_lb':atributo.tipo_control.nombre,'atributo_lb':atributo.atributo.nombre}
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def atributo_producto_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[8]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if ProductoAtributo.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=ProductoAtributo.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]                 
            else:
                data[dato]=None        
        
        atributo.atributo_id=data['atributo']
        atributo.tipo_control_id=data['tipo_control']
        #print(data)
        if atributo.has_changed==True:
            atributo.save(using=bd)
            respuesta={"respuesta":1,'tipo_control_lb':atributo.tipo_control.nombre,'atributo_lb':atributo.atributo.nombre}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if ProductoAtributo.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        atributo=ProductoAtributo.objects.using(bd).get(id=pk)
        atributo.estado=False
        atributo.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)

