from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'userauth/login.html'},
        name='userauth_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'},
        name='userauth_logout'),
    url(r'^change-password/$', 'password_change',
        {'template_name': 'userauth/password_change_form.html'},
        name='userauth_password_change'),
    url(r'^password-changed/$', 'password_change_done',
        {'template_name': 'userauth/password_change_done.html'},
        name='userauth_password_change_done')
)
