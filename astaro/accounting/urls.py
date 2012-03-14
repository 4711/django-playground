from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('accounting.views',
    url(r'^calctraffic/(?P<logday>today|yesterday)?$', 'calculated_traffic_list', name='accounting_calculated_traffic_index'),
    url(r'^calctraffic/(?P<logday>\d{4}-\d{2}-\d{2})?$', 'calculated_traffic_list', name='accounting_calculated_traffic_index'),

    url(r'^traffic/(?P<logday>today|yesterday)?$', 'traffic_list', name='accounting_traffic_index'),
    url(r'^traffic/(?P<logday>\d{4}-\d{2}-\d{2})?$', 'traffic_list', name='accounting_traffic_index'),

    url(r'^logins/$', 'login_list', name='accounting_login_index'),
    url(r'^logins/(?P<username>\w*)$', 'login_user_list', name='accounting_login_detail'),
)
