from django.shortcuts import render_to_response
from django.db.models import Count, Sum
from models import Authorization, Traffic, CalculatedTraffic


def dashboard(request):
    login_tot = Authorization.objects.count()
    login_ok = Authorization.objects.filter(authresult='ok').count()
    login_fail = login_tot - login_ok

    return render_to_response('dashboard.html', {'login_list': login_list, 'login_ok': login_ok, 'login_fail': login_fail, 'nav_name': 'dashboard'})


def calculated_traffic_list(request, logday=''):
    import datetime

    DATEFMT = '%Y-%m-%d'

    if not logday or logday == 'today':
        logday = datetime.datetime.today().strftime(DATEFMT)
    elif logday == 'yesterday':
        logday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATEFMT)

    nextday = (datetime.datetime.strptime(logday, DATEFMT) + datetime.timedelta(days=1)).strftime(DATEFMT)
    prevday = (datetime.datetime.strptime(logday, DATEFMT) - datetime.timedelta(days=1)).strftime(DATEFMT)

    traffic_tot = CalculatedTraffic.objects.filter(logday=logday).aggregate(Sum('traffic_in'), Sum('traffic_out'))
    traffic_list = CalculatedTraffic.objects.filter(logday=logday).order_by('-traffic_out')[:10]
    return render_to_response('accounting/calculated_traffic_list.html', {'logday': logday, 'nextday': nextday, 'prevday': prevday, 'traffic_list': traffic_list, 'total_in': traffic_tot.values()[0], 'total_out': traffic_tot.values()[1], 'nav_name': 'traffic_by_net'})


def traffic_list(request, logday=''):
    import datetime

    DATEFMT = '%Y-%m-%d'

    if not logday or logday == 'today':
        logday = datetime.datetime.today().strftime(DATEFMT)
    elif logday == 'yesterday':
        logday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATEFMT)

    nextday = (datetime.datetime.strptime(logday, DATEFMT) + datetime.timedelta(days=1)).strftime(DATEFMT)
    prevday = (datetime.datetime.strptime(logday, DATEFMT) - datetime.timedelta(days=1)).strftime(DATEFMT)

    traffic_tot = Traffic.objects.filter(logday=logday).aggregate(Sum('raw_out_pktlen'), Sum('raw_in_pktlen'))
    traffic_list = Traffic.objects.filter(logday=logday).values('srcip', 'dstip').annotate(bytes_out=Sum('raw_out_pktlen'), bytes_in=Sum('raw_in_pktlen')).order_by('-bytes_out')[:10]
    return render_to_response('accounting/traffic_list.html', {'logday': logday, 'nextday': nextday, 'prevday': prevday, 'traffic_list': traffic_list, 'traffic_in': traffic_tot.values()[0], 'traffic_out': traffic_tot.values()[1], 'nav_name': 'traffic_by_ip'})


def login_list(request):
    login_tot = Authorization.objects.count()
    login_ok = Authorization.objects.filter(authresult='ok').count()
    login_fail = login_tot - login_ok

    login_list = Authorization.objects.values('username', 'authresult').annotate(number_of_logins=Count('username')).order_by('username', 'authresult')

    return render_to_response('accounting/login_list.html', {'login_list': login_list, 'login_ok': login_ok, 'login_fail': login_fail, 'nav_name': 'logins'})


def login_user_list(request, username):

    login_tot = Authorization.objects.filter(username=username).count()
    login_ok = Authorization.objects.filter(username=username).filter(authresult='ok').count()
    login_fail = login_tot - login_ok

    login_list = Authorization.objects.filter(username=username).order_by('-logtime')

    return render_to_response('accounting/login_user_list.html', {'login_list': login_list, 'username': username, 'login_ok': login_ok, 'login_fail': login_fail, 'nav_name': 'logins'})
