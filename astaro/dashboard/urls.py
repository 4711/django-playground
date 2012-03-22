from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dashboard.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^search$', 'search_page', name='dashboard_search'),
    url(r'^ajax/autocomplete$', 'ajax_autocomplete', name='dashboard_autocomplete'),
)
