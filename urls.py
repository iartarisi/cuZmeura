from django.conf.urls.defaults import *

from ads.views import serve, index

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
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
