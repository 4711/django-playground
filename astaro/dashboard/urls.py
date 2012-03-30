from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^search$', 'search_page', name='dashboard_search'),
    url(r'^chart/(?P<year>\d{4})/(?P<month>\d{1,2})$', 'chart_view', name='dashboard_chart'),
    url(r'^chart_new$', 'chart_new', name='dashboard_chart'),
    url(r'^ajax/autocomplete$', 'ajax_autocomplete', name='dashboard_autocomplete'),
)
