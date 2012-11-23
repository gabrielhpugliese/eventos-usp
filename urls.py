from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^save_events/$', 'eventos.views.save_events'),
    url(r'^vote/(?P<event>.+)/$', 'eventos.views.vote'),
    url(r'^show_grade/(?P<event>.+)/$', 'eventos.views.show_grade'),
    url(r'^recommend/$', 'eventos.views.recommend'),
    url(r'^$', 'eventos.views.index'),
)

