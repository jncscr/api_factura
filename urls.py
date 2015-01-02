from django.conf.urls import patterns, url
 
from rest_framework.urlpatterns import format_suffix_patterns
 

urlpatterns = patterns('api_factura.views',
    url(r'^productos/$', 'producto_listado'), 
    url(r'^categorias/$', 'categoria_listado'), 
    url(r'^categorias/(?P<pk>[0-9]+)$', 'categoria_detalle'),  
    url(r'^caracteristicas/$', 'caracteristica_listado'),
    url(r'^caracteristicas/(?P<pk>[0-9]+)$', 'caracteristica_detalle'),
    url(r'^atributos/$', 'atributo_listado'),
    url(r'^atributos/(?P<pk>[0-9]+)$', 'atributo_detalle'),
    url(r'^atributos/valores/$', 'atributo_val_listado'),
    url(r'^atributos/valores/(?P<pk>[0-9]+)$', 'atributo_val_detalle'),
)

urlpatterns = format_suffix_patterns(urlpatterns)


