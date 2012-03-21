from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count, Sum
from models import Authorization, Traffic, CalculatedTraffic

import logging

logger = logging.getLogger(__name__)
logger.debug(': logger created')


@login_required
def calculated_traffic_index(request, logday=''):
    logger.debug(': log_index')
    import datetime

    DATEFMT = '%Y-%m-%d'

    logger.debug(': calculated_traffic_index')

    context = {}
    context['nav_name'] = 'traffic_by_net'

    if not logday or logday == 'today':
        context['logday'] = datetime.datetime.today()
    elif logday == 'yesterday':
        context['logday'] = datetime.datetime.today() - datetime.timedelta(days=1)
    else:
        context['logday'] = datetime.datetime.strptime(logday, DATEFMT)

    context['nextday'] = (context['logday'] + datetime.timedelta(days=1)).strftime(DATEFMT)
    context['prevday'] = (context['logday'] - datetime.timedelta(days=1)).strftime(DATEFMT)

    context['traffic_tot'] = CalculatedTraffic.objects.filter(logday=logday).aggregate(Sum('traffic_in'), Sum('traffic_out'))
    context['traffic_list'] = CalculatedTraffic.objects.filter(logday=logday).order_by('-traffic_out')[:10]
    context['traffic_in'] = context['traffic_tot'].values()[0]
    context['traffic_out'] = context['traffic_tot'].values()[1]

    return render_to_response('accounting/calculated_traffic_list.html', context,
        context_instance=RequestContext(request))


@login_required
def traffic_index(request, logday=''):
    logger.debug(': log_index')
    import datetime

    DATEFMT = '%Y-%m-%d'

    context = {}
    context['nav_name'] = 'traffic_by_ip'

    if not logday or logday == 'today':
        context['logday'] = datetime.datetime.today()
    elif logday == 'yesterday':
        context['logday'] = datetime.datetime.today() - datetime.timedelta(days=1)
    else:
        context['logday'] = datetime.datetime.strptime(logday, DATEFMT)

    context['nextday'] = (context['logday'] + datetime.timedelta(days=1)).strftime(DATEFMT)
    context['prevday'] = (context['logday'] - datetime.timedelta(days=1)).strftime(DATEFMT)

    context['traffic_tot'] = Traffic.objects.filter(logday=logday).aggregate(Sum('raw_out_pktlen'), Sum('raw_in_pktlen'))
    context['traffic_list'] = Traffic.objects.filter(logday=logday).values('srcip', 'dstip').annotate(bytes_out=Sum('raw_out_pktlen'), bytes_in=Sum('raw_in_pktlen')).order_by('-bytes_out')[:50]
    context['traffic_in'] = context['traffic_tot'].values()[0]
    context['traffic_out'] = context['traffic_tot'].values()[1]

    return render_to_response('accounting/traffic_list.html', context,
        context_instance=RequestContext(request))


@login_required
def login_index(request):
    logger.debug(': log_index')
    context = {}
    context['nav_name'] = 'logins'
    context['login_tot'] = Authorization.objects.count()
    context['login_ok'] = Authorization.objects.filter(authresult='ok').count()
    context['login_fail'] = context['login_tot'] - context['login_ok']
    context['login_list'] = Authorization.objects.values('username', 'authresult').annotate(number_of_logins=Count('username')).order_by('username', 'authresult')

    #logger.debug('Logins: %d/%d/%d' % (context['login_tot'], context['login_ok'], context['login_fail']))

    return render_to_response('accounting/login_list.html', context,
        context_instance=RequestContext(request))


@login_required
def login_user_list(request, username):
    context = {}
    context['nav_name'] = 'logins'
    context['login_tot'] = Authorization.objects.filter(username=username).count()
    context['login_ok'] = Authorization.objects.filter(username=username).filter(authresult='ok').count()
    context['login_fail'] = context['login_tot'] - context['login_ok']
    context['login_list'] = Authorization.objects.filter(username=username).order_by('-logtime')

    return render_to_response('accounting/login_user_list.html', context,
        context_instance=RequestContext(request))
