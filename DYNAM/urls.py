
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'load', 'DYNAM.views.load'),
                       url(r'flood', 'DYNAM.views.flood'),
                        url(r'chart1', 'DYNAM.views.chart1'),
                       url(r'', 'DYNAM.views.load')
                       )