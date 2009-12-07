from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from ads.views import serve

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template' : 'index.html'}),
                       
    (r'^serve/(\w+)?$', serve),
                       
#    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#        {'document_root': '/home/mapleoin/flossad/static'}),

    # Example:
    # (r'^flossad/', include('flossad.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
