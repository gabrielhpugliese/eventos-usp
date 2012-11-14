from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^salvar_eventos/$', 'eventos.views.salvar_eventos'),
    url(r'^votar/(?P<evento>.+)/$', 'eventos.views.votar'),
    url(r'^pegar_nota/(?P<evento>.+)/$', 'eventos.views.pegar_nota'),
)

