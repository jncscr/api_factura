from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedCaracteristicaSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
from django.db.models import Q
from api_factura.models import Caracteristica

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


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
        print(request.QUERY_PARAMS)
        if request.QUERY_PARAMS.get('param') is not None:
            
            param=request.QUERY_PARAMS.get('param')
            caracteristicas = Caracteristica.objects.using(bd).filter(Q(estado=True),
                                                        Q(nombre__icontains = param))            
        else:
            caracteristicas = Caracteristica.objects.using(bd).filter(estado=True)
        #print(len(personal))
        numPages=request.QUERY_PARAMS.get('per_page')
        paginator = Paginator(caracteristicas,numPages)
        
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
        serializer = PaginatedCaracteristicaSerializer(registros,
                                             context=serializer_context)
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

