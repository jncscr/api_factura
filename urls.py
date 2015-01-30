from django.conf.urls import patterns, url
 
from rest_framework.urlpatterns import format_suffix_patterns
 

urlpatterns = patterns('api_factura.views',
    url(r'^productos/$', 'producto_listado'), 
    url(r'^productos/(?P<pk>[0-9]+)$', 'producto_detalle'),
    url(r'^categorias/$', 'categoria_listado'), 
    url(r'^categorias/(?P<pk>[0-9]+)$', 'categoria_detalle'),  
    url(r'^categorias/productos/lista/$', 'categoria_producto_lista'),
    url(r'^categorias/productos/$', 'categoria_producto'),
    url(r'^caracteristicas/$', 'caracteristica_listado'),
    url(r'^caracteristicas/(?P<pk>[0-9]+)$', 'caracteristica_detalle'),
    url(r'^caracteristicas/productos/$', 'caracteristica_producto_listado'),
    url(r'^caracteristicas/productos/(?P<pk>[0-9]+)$', 'caracteristica_producto_detalle'),
    url(r'^atributos/$', 'atributo_listado'),
    url(r'^atributos/(?P<pk>[0-9]+)$', 'atributo_detalle'),
    url(r'^atributos/valores/$', 'atributo_val_listado'),
    url(r'^atributos/valores/(?P<pk>[0-9]+)$', 'atributo_val_detalle'),
    url(r'^atributos/productos/$', 'atributo_producto_listado'),
    url(r'^atributos/productos/(?P<pk>[0-9]+)$', 'atributo_producto_detalle'),
    url(r'^proveedores/$', 'proveedor_listado'), 
    url(r'^proveedores/(?P<pk>[0-9]+)$', 'proveedor_detalle'),
    url(r'^clientes/$', 'cliente_listado'), 
    url(r'^clientes/(?P<pk>[0-9]+)$', 'cliente_detalle'),
)

urlpatterns = format_suffix_patterns(urlpatterns)


