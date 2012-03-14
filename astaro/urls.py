from django.conf.urls.defaults import patterns, include, url
from accounting.views import dashboard, login_list, login_user_list, traffic_list, calculated_traffic_list

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

    url(r'^$', dashboard),

    url(r'^accounting/calctraffic/(?P<logday>today|yesterday)?$', calculated_traffic_list),
    url(r'^accounting/calctraffic/(?P<logday>\d{4}-\d{2}-\d{2})?$', calculated_traffic_list),

    url(r'^accounting/traffic/(?P<logday>today|yesterday)?$', traffic_list),
    url(r'^accounting/traffic/(?P<logday>\d{4}-\d{2}-\d{2})?$', traffic_list),

    url(r'^accounting/logins/$', login_list),
    url(r'^accounting/logins/(?P<username>\w*)$', login_user_list),
)
