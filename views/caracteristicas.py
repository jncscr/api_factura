from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedCaracteristicaSerializer
from api_factura.serializers import PaginatedProductoCaracteristicaSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
from django.db.models import Q
from api_factura.models import Caracteristica,ProductoCaracteristica

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import connections

@api_view(['GET', 'POST'])
def caracteristica_listado(request):
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
            caracteristicas = Caracteristica.objects.using(bd).filter(Q(estado=True),
                                                        (Q(nombre__icontains = param)|
                                                        Q(id__icontains=param)))            
        else:
            caracteristicas = Caracteristica.objects.using(bd).filter(estado=True)
        #print(len(personal))
        numRegistros=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(caracteristicas,numRegistros)
        
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
        serializer = PaginatedCaracteristicaSerializer(registros,
                                             context=serializer_context)
        if request.QUERY_PARAMS.get('sin_total')==None:
            num=0
            conn = connections[bd]
            if conn.connection is None:
                cursor = conn.cursor()        
            cursor = conn.connection.cursor()
            query ='select count(caracteristica.id) \n\
                    from caracteristica where caracteristica.estado=1'
            cursor.execute(query)
            row =cursor.fetchone()
            if row[0]!=None:
                num=row[0]
            num=num+1
            serializer.data['last_num_reg']=num;
        
        return Response(serializer.data)
    
    elif request.method=='POST':
        data={}        
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        caracteristica=Caracteristica(nombre=data['nombre'],
                        estado=True)
        
        caracteristica.save(using=bd)
        respuesta={"id":caracteristica.id}
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def caracteristica_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if Caracteristica.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        caracteristica=Caracteristica.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        
        caracteristica.nombre=data['nombre']
        #print(data)
        if caracteristica.has_changed==True:
            caracteristica.save(using=bd)
            respuesta={"respuesta":1}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if Caracteristica.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        caracteristica=Caracteristica.objects.using(bd).get(id=pk)
        caracteristica.estado=False
        caracteristica.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def caracteristica_producto_listado(request):
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
            caracteristicas = ProductoCaracteristica.objects.using(bd).filter(Q(estado=True),
                                                        Q(caracteristica__estado=True),
                                                        Q(producto_id=id_prod),
                                                        (Q(caracteristica__nombre__icontains = param)|
                                                        Q(id__icontains=param)))            
        else:
            caracteristicas = ProductoCaracteristica.objects.using(bd).filter(estado=True,
                                                                            caracteristica__estado=True,
                                                                            producto_id=id_prod)
        #print(len(personal))
        numRegistros=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(caracteristicas,numRegistros)
        
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
        serializer = PaginatedProductoCaracteristicaSerializer(registros,
                                             context=serializer_context)
        num=0
        conn = connections[bd]
        if conn.connection is None:
            cursor = conn.cursor()        
        cursor = conn.connection.cursor()
        query ='select count(producto_caracteristica.id) \n\
                from caracteristica,producto_caracteristica where \n\
                producto_caracteristica.estado=1 and producto_caracteristica.producto_id=%s and \n\
                caracteristica.id=producto_caracteristica.caracteristica_id and \n\
                caracteristica.estado=1'
        cursor.execute(query,[id_prod])
        row =cursor.fetchone()
        if row[0]!=None:
            num=row[0]
        num=num+1
        serializer.data['last_num_reg']=num;
        return Response(serializer.data)
    
    elif request.method=='POST':
        data={}        
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        productoCar=ProductoCaracteristica(producto_id=data['producto_id'],
                        caracteristica_id=data['caracteristica'],
                        valor=data['valor'],
                        estado=True)
        
        productoCar.save(using=bd)
        respuesta={"id":productoCar.id,"nombre":productoCar.caracteristica.nombre}
        return Response(respuesta, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def caracteristica_producto_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[8]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if ProductoCaracteristica.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        caracteristica=ProductoCaracteristica.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        
        caracteristica.producto_id=data['producto_id']
        caracteristica.caracteristica_id=data['caracteristica']
        caracteristica.valor=data['valor']
        #print(data)
        if caracteristica.has_changed==True:
            caracteristica.save(using=bd)
            respuesta={"respuesta":1,'nombre':caracteristica.caracteristica.nombre}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if ProductoCaracteristica.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        caracteristica=ProductoCaracteristica.objects.using(bd).get(id=pk)
        caracteristica.estado=False
        caracteristica.save(using=bd)        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)
