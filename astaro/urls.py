from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from accounting.views import dashboard

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^grappelli/', include('grappelli.urls')),

    url(r'^$', redirect_to, {'url': '/user/login'}),
    url(r'^dashboard$', dashboard, name='dashboard'),
    url(r'^accounting/', include('accounting.urls')),
    url(r'^user/', include('userauth.urls')),
)
