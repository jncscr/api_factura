from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedPersonalSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
from django.db.models import Q
from api_factura.models import Personal

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['GET', 'POST'])
def cliente_listado(request):
    #from api_pollo.models import Personal
    #Codigo de verificacion de asignacion de modulo    
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[11]
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
            personal = Personal.objects.using(bd).filter(Q(estado=True),
                                                        Q(tipo=1),
                                                        Q(cliente_proveedor=False),
                                                        Q(id__icontains=param) |
                                                        Q(nombres__icontains = param) |
                                                        Q(apellidos__icontains=param) | 
                                                        Q(empresa__icontains=param) |
                                                        Q(telefono__icontains=param))
            if len(personal)==0:
                param="%"+param+"%"
                personal = Personal.objects.using(bd).extra(where=["(CONCAT(CONCAT(nombres,' '),apellidos)) LIKE %s and cliente_proveedor=0 "], params=[param])  
                
        else:
            personal = Personal.objects.using(bd).filter(estado=True,
                                                        tipo=1,
                                                        cliente_proveedor=False)
        #print(len(personal))
        paginator = Paginator(personal, 10)
        
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
        serializer = PaginatedPersonalSerializer(registros,
                                             context=serializer_context)
        return Response(serializer.data)
    
    elif request.method=='POST':
        fecha=datetime.now().strftime("%Y-%m-%d")
        data={}
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='nit':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        personal=Personal(nombres=data['nombres'],
                        apellidos=data['apellidos'],
                        empresa=data['empresa'],
                        telefono=data['telefono'],
                        direccion=data['direccion'],
                        nit=data['nit'],
                        usuario_sistema_id=user.id,
                        estado=True,
                        tipo=1,
                        empresa_id=user.empresa.id,
                        fecha=fecha,
                        cliente_proveedor=False)
        
        personal.save(using=bd)
        respuesta={"id":personal.id}
        return Response(respuesta, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
def cliente_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[11]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    print(modulo_valido)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if Personal.objects.using(bd).filter(id=pk, estado=True,tipo=1).exists() is not True:
            errors={"error":"El cliente ha sido borrado, o no esta registrado en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        personal=Personal.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='nit':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        personal.nombres=data['nombres']
        personal.apellidos=data['apellidos']
        personal.empresa=data['empresa']
        personal.telefono=data['telefono']
        personal.direccion=data['direccion']
        personal.nit=data['nit']
        print(personal.has_changed)
        if personal.has_changed==True:
            personal.save(using=bd)
            respuesta={"respuesta":1}
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            respuesta={"respuesta":2}
            return Response(respuesta, status=status.HTTP_200_OK)
        
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if Personal.objects.using(bd).filter(id=pk, estado=True,tipo=1).exists() is not True:
            errors={"error":"El cliente ha sido borrado, o no esta registrado en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        personal=Personal.objects.using(bd).get(id=pk)
        personal.estado=False
        personal.save(using=bd)
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)
            