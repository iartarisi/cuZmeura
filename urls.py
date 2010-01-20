from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from ads.serve import serve
from ads.user import confirm, profile, register

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template' : 'index.html',
                                 'extra_context': {
                                     'domain':'http://pristav.ceata.org/',
                                     'pubslug': 'pristav'}
                                 }),

    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page' : '/'}),
                       
    (r'^serve/(\w+)?/?(\d+x\d+)?$', serve),

    # User actions
    (r'^user/profile/$', profile),
    (r'^user/register/$', register),
    (r'^user/confirm/(\w+)$', confirm),

    # Django contrib.admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Uncomment these lines when in 'development mode'
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': '/home/mapleoin/pristav/media'}),


)
