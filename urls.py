from django.conf.urls import patterns, url
 
from rest_framework.urlpatterns import format_suffix_patterns
 

urlpatterns = patterns('api_factura.views',
    url(r'^productos/$', 'producto_listado'), 
    url(r'^categorias/$', 'categoria_listado'), 
    url(r'^categorias/(?P<pk>[0-9]+)$', 'categoria_detalle'),  
    #url(r'^cobros/(?P<pk>[0-9]+)$', 'cobro_detalle'),   
    #url(r'^compras/$', 'compras_listado'),
    #url(r'^compras/(?P<pk>[0-9]+)$', 'compras_detalle'),
    #url(r'^compras/reporte/$', 'compras_reporte'),
    #url(r'^compras/asignacion/$', 'compra_asignacion_listado'),
    #url(r'^compras/asignacion/(?P<pk>[0-9]+)$', 'compra_asignacion_detalle'),
)

urlpatterns = format_suffix_patterns(urlpatterns)


