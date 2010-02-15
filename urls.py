from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from ads.serve import serve
from ads.user import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template' : 'index.html',
                                 'extra_context': {
                                     'domain':'http://localhost:8000/',
                                     }
                                 }),

    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page' : '/'}),
                       
    (r'^serve/(\w+)?/?(\d+x\d+)?$', serve),

    # User actions
    (r'^user/profile/$', profile),

    (r'^user/product/(\w+)/$', product),
    (r'^user/register/$', register),
    (r'^user/confirm/(\w+)$', confirm),
                      
#    (r'^user/pub/add/$', create_pub),
    (r'^user/pub/edit/(\w+)$', update_pub),
    (r'^user/pub/remove/(\w+)$', delete_pub),

    # Django contrib.admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # serve static pages in development mode
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/home/mapleoin/cuZmeura/media'}),
    )
