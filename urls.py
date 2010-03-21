from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from ads.index import index
from ads.serve import serve_ad
from ads.user import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^about/$', direct_to_template, { 'template': 'about.html'}),
                       
    (r'^serve/(\w+)?/?(\d+x\d+)?$', serve_ad),

    # User actions
    (r'^user/profile/$', profile),

    (r'^user/product/(\w+)/$', product),
    (r'^user/register/$', register),
    (r'^user/confirm/(\w+)$', confirm),
                       
    (r'^user/pub/remove/([-\w]+)$', delete_pub),
    (r'^user/pub/modify/([-\w]+)$', modify_pub),                   

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
