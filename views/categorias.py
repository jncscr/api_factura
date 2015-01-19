#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api_factura.serializers import PaginatedProductoSerializer
from api_usuario.models import Usuario
from api_pollo.views.validar_modulos import validar_modulos
#from django.db.models import Q
from api_factura.models import ProductoCategoria

#Usuario,PerfilModulo,EmpresaModulo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db import connections

@api_view(['GET', 'POST'])
def categoria_listado(request):
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
        id_cat=0
        if request.QUERY_PARAMS.get('id') is not None:
            id_cat=int(request.QUERY_PARAMS.get('id'))
        categorias=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=True,
                                                        estado=True).order_by("numero")
        texto='<ul>'
        if id_cat==0:
            texto=texto+'<li>'+'<input checked="checked" type="radio" name="categoria" value="0" data-radio="Principal"/>\n\
                        <span style="box-shadow: 0.2px 0.2px 6.2px #16a085;"><i class="fa fa-folder-open"></i> Principal</span>'
        else:
            texto=texto+'<li>'+'<input type="radio" name="categoria" value="0" data-radio="Principal"/>\n\
                    <span><i class="fa fa-folder-open"></i> Principal</span>'
        arbol=crearArbol(categorias,bd,id_cat)
        texto=texto+arbol+'</li></ul>'
        respuesta = {'Arbol': texto}
        
        return Response(respuesta)
    
    elif request.method=='POST':
        #print(request.DATA)
        data={}
        for dato in request.DATA:
            if request.DATA[dato]!='':
                if dato=='categoria':
                    data[dato]=int(request.DATA[dato])
                else:
                    data[dato]=request.DATA[dato]  
            else:
                data[dato]=None     
    
        conn = connections[bd]
        if conn.connection is None:
            cursor = conn.cursor()        
        cursor = conn.connection.cursor()
        numero=0
        es_nodo_principal=False
        producto_categoria=None
        if data['categoria']==0:
            query ='select count(producto_categoria.id) \n\
                    from producto_categoria where producto_categoria.estado=1\n\
                    and producto_categoria.es_nodo_principal=1'
            
            cursor.execute(query)
            row =cursor.fetchone()
            if row[0]!=None:
                numero=int(row[0])+1
            cursor.close()
            es_nodo_principal=True
        else:
            query ='select count(producto_categoria.id) \n\
                    from producto_categoria where producto_categoria.estado=1\n\
                    and producto_categoria.producto_categoria_id=%s'            
            cursor.execute(query,[data['categoria']])
            row =cursor.fetchone()
            if row[0]!=None:
                numero=int(row[0])+1
            cursor.close()
            producto_categoria=data['categoria']
            
        categoria=ProductoCategoria(nombre=data['nombre'],
                numero=numero,
                estado=True,
                es_nodo_principal=es_nodo_principal,
                producto_categoria_id=producto_categoria)
        
        categoria.save(using=bd)
        respuesta={"id":categoria.id}
        return Response(respuesta, status=status.HTTP_201_CREATED)

def crearArbol(categorias,bd,id_cat):
    texto='<ul>'
    for cat in categorias:
               
        subcategorias=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=False,
                                                        estado=True,
                                                        producto_categoria_id=cat.id).order_by("numero")
        subsTexto=''
        
        if len(subcategorias)>0:
            subsTexto=crearArbol(subcategorias,bd,id_cat)
            if cat.id==id_cat:
                texto=texto+'<li>'+'<input checked="checked" type="radio" name="categoria" value="'+str(cat.id)+'" data-radio="'+cat.nombre+'" data-numero="'+str(cat.numero)+'" />\n\
                        <span style="box-shadow: 0.2px 0.2px 6.2px #16a085;"><i class="fa fa-folder-open"></i> '+cat.nombre+' </span>'
            else:
                texto=texto+'<li>'+'<input type="radio" name="categoria" value="'+str(cat.id)+'" data-radio="'+cat.nombre+'" data-numero="'+str(cat.numero)+'" />\n\
                    <span><i class="fa fa-folder-open"></i> '+cat.nombre+' </span>'
        else:
            if cat.id==id_cat:
                texto=texto+'<li>'+'<input checked="checked" type="radio" name="categoria" value="'+str(cat.id)+'" data-radio="'+cat.nombre+'" data-numero="'+str(cat.numero)+'" />\n\
                        <span style="box-shadow: 0.2px 0.2px 6.2px #16a085;"><i class="fa fa-tag"></i> '+cat.nombre+' </span>'
            else:
                texto=texto+'<li>'+'<input type="radio" name="categoria" value="'+str(cat.id)+'" data-radio="'+cat.nombre+'" data-numero="'+str(cat.numero)+'" />\n\
                    <span><i class="fa fa-tag"></i> '+cat.nombre+' </span>'
        texto=texto+subsTexto+'</li>';
        
    texto=texto+'</ul>'
    
    return texto

@api_view(['PUT', 'DELETE'])
def categoria_detalle(request,pk):
    user=Usuario.objects.get(auth_user_id=request.user.id)
    
    modulos=[9]
    modulo_valido=validar_modulos(user.perfil.id,user.empresa.id,modulos)
    if modulo_valido['error']==1:
        errors={"error":"No tiene permisos suficientes, para realizar operaciones en este modulo"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    bd=modulo_valido['bd']
    
    if request.method == 'PUT':
        data={}
        if ProductoCategoria.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        categoria=ProductoCategoria.objects.using(bd).get(id=pk)
        #print(personal['apellidos'])
        for dato in request.DATA:
            if request.DATA[dato]!='':
                data[dato]=request.DATA[dato]  
            else:
                data[dato]=None        
        
        if data['numero']==0:
            categoria.nombre=data['nombre']
            #print(data)
            if categoria.has_changed==True:
                categoria.save(using=bd)
                respuesta={"respuesta":1}
                return Response(respuesta, status=status.HTTP_200_OK)
            else:
                respuesta={"respuesta":2}
                return Response(respuesta, status=status.HTTP_200_OK)
        elif data['numero']==1:
            numero=categoria.numero
            if numero!=1:
                numero=numero-1
                if categoria.producto_categoria==None:
                    cats=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=True,
                                                        estado=True,
                                                        numero=numero)
                    for cat in cats:
                        cat.numero=numero+1;
                        cat.save(using=bd)
                else:
                    cats=ProductoCategoria.objects.using(bd).filter(estado=True,
                                                        numero=numero,
                                                        producto_categoria_id=categoria.producto_categoria.id)
                    for cat in cats:
                        cat.numero=numero+1;
                        cat.save(using=bd)
                        #print(cat)
                categoria.numero=numero
                categoria.save(using=bd)
                respuesta={"respuesta":1}
                return Response(respuesta, status=status.HTTP_200_OK)
            else:
                respuesta={"respuesta":2}
                return Response(respuesta, status=status.HTTP_200_OK)
        elif data['numero']==2:
            numero=categoria.numero
            numero=numero+1
            cats=[]
            if categoria.producto_categoria==None:
                cats=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=True,
                                                    estado=True,
                                                    numero=numero)
                for cat in cats:
                    cat.numero=numero-1;
                    cat.save(using=bd)
            else:
                cats=ProductoCategoria.objects.using(bd).filter(estado=True,
                                                    numero=numero,
                                                    producto_categoria_id=categoria.producto_categoria.id)
                for cat in cats:
                    cat.numero=numero-1;
                    cat.save(using=bd)
                    #print(cat)
            if len(cats)>0:
                categoria.numero=numero
                categoria.save(using=bd)
                respuesta={"respuesta":1}
            else:
                respuesta={"respuesta":3}
            return Response(respuesta, status=status.HTTP_200_OK)
            #return Response(respuesta, status=status.HTTP_200_OK)
            
        errors={"error":""}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if ProductoCategoria.objects.using(bd).filter(id=pk, estado=True).exists() is not True:
            errors={"error":"El registro ha sido borrado, o no existe en el sistema"}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        categoria=ProductoCategoria.objects.using(bd).get(id=pk)
        categoria.estado=False
        categoria.save(using=bd)
        
        numero=categoria.numero        
        cats=[]
        if categoria.producto_categoria==None:
            cats=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=True,
                                                estado=True,
                                                numero__gt=numero)
            for cat in cats:
                cat.numero=cat.numero-1;
                cat.save(using=bd)
        else:
            cats=ProductoCategoria.objects.using(bd).filter(estado=True,
                                                numero__gt=numero,
                                                producto_categoria_id=categoria.producto_categoria.id)
            for cat in cats:
                cat.numero=cat.numero-1;
                cat.save(using=bd)
                #print(cat)
        
        respuesta={"":""}
        return Response(respuesta, status=status.HTTP_200_OK)

@api_view(['GET'])
def categoria_producto_lista(request):
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
        categorias=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=True,
                                                        estado=True).order_by("numero")
        texto='<ul class="dropdown-menu inner selectpicker" style="max-height: 220px; overflow-y: auto; min-height: 81px;" role="menu">'
        texto=texto+'<li class="btn-group open active">'+'<a data-cat="0" data-text="Todas"><span class="text">Todas</span></a>'
        num=1
        array=[]
        arbol=crearArbolLista(categorias,bd,num,0,array)
        texto=texto+arbol+'</li></ul>'
        respuesta = {'arbol': texto}
        
        return Response(respuesta)
    
def crearArbolLista(categorias,bd,num,sub,array):
    texto='<ul class="dropdown-menu inner" role="menu">'
    for cat in categorias:
               
        subcategorias=ProductoCategoria.objects.using(bd).filter(es_nodo_principal=False,
                                                        estado=True,
                                                        producto_categoria_id=cat.id).order_by("numero")
        subsTexto=''
        addNum=''
        si=False
        
        if sub==0:
            addNum=str(num)
            si=True
            array.append(num)
        else:
            if len(array)>0:
                addNum=str(array[0])
                for n in range(0,len(array)):
                    if n>0:
                        addNum=addNum+'.'+str(array[n])
        
        if len(subcategorias)>0:
            tmp_sub=sub
            tmp=[]
            for a in array:
                tmp.append(a)
            sub=1
            array.append(sub)
            subsTexto=crearArbolLista(subcategorias,bd,num,sub,array)
            array=tmp  
            sub=tmp_sub+1
            array[(len(array)-1)]=sub
            texto=texto+'<li class="btn-group open">'+'<a data-cat="'+str(cat.id)+'" data-text="'+cat.nombre+'"><span class="text">'+addNum+'. '+cat.nombre+'</span></a>'
            texto=texto+subsTexto+'<li class="divider" data-original-index="null"></li>'            
        else:
            texto=texto+'<li>'+'<a data-cat="'+str(cat.id)+'" data-text="'+cat.nombre+'"><span class="text">'+addNum+'. '+cat.nombre+'</span></a>'
            texto=texto+subsTexto+'</li>';            
            sub=sub+1
            array[(len(array)-1)]=sub
        if si==True: 
            sub=0
            array=[]
        
        num=num+1
    texto=texto+'</ul>'
    
    return texto
