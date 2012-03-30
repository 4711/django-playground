from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Count, Sum
from accounting.models import Authorization, PacketFilter, Traffic   # IntrusionCount, Traffic
from forms import SearchForm
from chartit import DataPool, Chart
from datetime import date


def dashboard(request):
    context = {}
    context['nav_name'] = 'dashboard'
    context['login_tot'] = Authorization.objects.count()
    context['login_ok'] = Authorization.objects.filter(authresult='ok').count()
    context['login_fail'] = context['login_tot'] - context['login_ok']

    """
    #Step 1: Create a DataPool with the data we want to retrieve.
    logindata = DataPool(series=[
      #{'options': {'source': IntrusionCount.objects.all()[:10]},
      {'options': {'source':  PacketFilter.objects.filter(logday='2012-03-01')[:10]},
                   'terms': ['logday', 'packets']
      }
    ])

    #Step 2: Create the Chart object
    cht1 = Chart(datasource=logindata, series_options=[
      {'options':{'type': 'spline', 'stacking': False}, 'terms':{'logday':['packets']}}],
      chart_options={'title': {'text': 'Rule Violations'},
      'credits': {'enabled': False},
      'xAxis': {'title': {'text': 'Day'}}}
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


def chart_view(request, year=2012, month=3):
    DATEFMT = '%Y-%m-01'

    logmonth = date(int(year), int(month), 1)

    context = {}
    context['nav_name'] = 'dashboard'
    context['year'] = int(year)
    context['month'] = int(month)
    thismonth = date(logmonth.year, logmonth.month, 1).strftime(DATEFMT)
    nextmonth = date(logmonth.year, logmonth.month + 1, 1).strftime(DATEFMT)

    context['drops'] = PacketFilter.objects.filter(logday__gte=thismonth, logday__lt=nextmonth).values('logday').annotate(tot=Sum('packets')).order_by('logday')[:35]
    context['traffic'] = Traffic.objects.filter(logday__gte=thismonth, logday__lt=nextmonth).values('logday').annotate(raus=Sum('raw_out_pktlen'), rein=Sum('raw_in_pktlen')).order_by('logday')[:35]

    return render_to_response('dashboard/chart.html', context,
        context_instance=RequestContext(request))
    #return render('dashboard/chart.html', context1)


def chart_new(request):

    context = {}
    context['nav_name'] = 'dashboard'
    chart = MyHighchart()
    context['chart'] = chart

    return render('dashboard/chart_new.html', context)
#    return render_to_response('dashboard/chart_new.html', context,
#        context_instance=RequestContext(request))


class MyHighchart(object):
    def __init__(self):
        self._render_to = 'chart'
        self._title = 'Title'
        self._subtitle = 'Sub Title'
        self._max_zoom = 14 * 24 * 3600 * 1000  # 14 days
        self._x_axis_title = 'x Axis'
        self._y_axis_title = 'y Axis'
        self._series_name = 'series_name'
        self._series_point_interval = 24 * 3600 * 1000

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @title.deleter
    def title(self):
        del self._title

    def render(self):
        return """var chart;
    chart = new Highcharts.Chart({
        chart: {
            renderTo: '%(render_to)s',
            zoomType: 'x',
            spacingRight: 20
        },
        title: {
            text: '%(title)s'
        },
        subtitle: {
            text: '%(subtitle)s'
        },
        credits: {
            enabled: false
        },
        xAxis: {
            type: 'datetime',
            maxZoom: %(max_zoom)d,
            title: {
                text: '%(x_axis_title)s'
            }
        },
        yAxis: {
            title: {
                text: '%(y_axis_title)s'
            },
            min: 0.6,
            startOnTick: false,
            showFirstLabel: false
        },
        tooltip: {
            crosshairs: true,
            shared: true
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, 'rgba(2,0,0,0)']
                    ]
                },
                lineWidth: 1,
                marker: {
                    enabled: false,
                    states: {
                        hover: {
                            enabled: true,
                            radius: 5
                        }
                    }
                },
                shadow: false,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                }
            }
        },

        series: [{
            type: 'area',
            name: 'Dropped Packets',
            pointInterval: %(series_point_interval)d,
            pointStart: Date.UTC(2012, 2, 1),
            data: [ 1, 2, 3, 4, 5, 6, 7, 8 ]
        }]
    });
    """ % {'render_to': self._render_to, 'title': self.title, 'subtitle': self._subtitle, 'max_zoom': self._max_zoom,
           'x_axis_title': self._x_axis_title, 'y_axis_title': self._y_axis_title, 'series_point_interval': self._series_point_interval}
