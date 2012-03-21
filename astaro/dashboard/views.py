from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Count
from accounting.models import Authorization
from forms import SearchForm


def dashboard(request):
    context = {}
    context['nav_name'] = 'dashboard'
    context['login_tot'] = Authorization.objects.count()
    context['login_ok'] = Authorization.objects.filter(authresult='ok').count()
    context['login_fail'] = context['login_tot'] - context['login_ok']

    return render_to_response('dashboard/index.html', context,
        context_instance=RequestContext(request))


def  search_page(request):
    context = {}
    context['nav_name'] = 'dashboard'
    context['form'] = SearchForm()
    context['show_results'] = False
    if 'query' in request.GET:
        context['show_results'] = True
        context['query'] = request.GET['query'].strip()
        if context['query']:
            context['form'] = SearchForm({'query': context['query']})
            #context['logins'] = Authorization.objects.filter(username__startswith=context['query']).values('username').distinct()
            context['logins'] = Authorization.objects.filter(username__startswith=context['query']).values('username', 'authresult').annotate(number_of_logins=Count('username')).order_by('username', 'authresult')

    return render_to_response('dashboard/search.html', context,
        context_instance=RequestContext(request))


def ajax_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET['query'].strip()
        logins = Authorization.objects.filter(username__startswith=query)[:10]
        return HttpResponse('\n'.join(login.username for login in logins))
    return HttpResponse()
