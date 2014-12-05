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
            if request.DATA[dato]!='':
                if dato=='nit':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        personal=Producto(nombres=data['nombres'],
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
