from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Count
from accounting.models import Authorization, IntrusionCount, Traffic
from forms import SearchForm
from chartit import DataPool, Chart


def dashboard(request):
    context = {}
    context['nav_name'] = 'dashboard'
    context['login_tot'] = Authorization.objects.count()
    context['login_ok'] = Authorization.objects.filter(authresult='ok').count()
    context['login_fail'] = context['login_tot'] - context['login_ok']

    #Step 1: Create a DataPool with the data we want to retrieve.
    logindata = DataPool(series=[
      {'options': {'source': IntrusionCount.objects.all()[:10]},
                   'terms': ['ruleid', 'count']
      }
    ])

    #Step 2: Create the Chart object
    cht1 = Chart(datasource=logindata, series_options=[
      {'options':{'type': 'line', 'stacking': False}, 'terms':{'ruleid':['count']}}],
      chart_options={'title': {'text': 'Rule Violations'},
      'xAxis': {'title': {'text': 'Rule-Id'}}}
    )
    """
    #Step 1: Create a DataPool with the data we want to retrieve.
    logindata = DataPool(series=[
      {'options': {'source': Traffic.objects.all()[:10]},
                   'terms': ['logday', 'raw_out_pktlen']
      }
    ])

    #Step 2: Create the Chart object
    cht1 = Chart(datasource=logindata, series_options=[
      {'options':{'type': 'line', 'stacking': False}, 'terms':{'logday':['raw_out_pktlen']}}],
      chart_options={'title': {'text': 'Traffic'},
      'xAxis': {'type': 'datetime',
      'title': {'text': 'Raw Packet Len'}}}
    )
    """

    #Step 3: Send the chart object to the template.
    context['loginchart'] = cht1

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


def chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    logindata = \
        DataPool(
           series=
            [{'options': {
               'source':  Authorization.objects.all().values('username', 'authresult').annotate(number_of_logins=Count('username')).order_by('username', 'authresult')},
              'terms': [
                'username',
                'authresult',
                'number_of_logins']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = logindata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'username': [
                    'number_of_logins' ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'User Logins'},
               'xAxis': {
                    'title': {
                       'text': 'User'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response({'loginchart': cht})

