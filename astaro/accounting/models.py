# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

PROTOCOL_CHOICES = (
    (0,      'ip'),
    (1,      'icmp'),
    (2,      'igmp'),
    (3,      'ggp'),
    (4,      'ipencap'),
    (5,      'st'),
    (6,      'tcp'),
    (8,      'egp'),
    (9,      'igp'),
    (12,    'pup'),
    (17,    'udp'),
    (20,    'hmp'),
    (22,    'xns-idp'),
    (27,    'rdp'),
    (29,    'iso-tp4'),
    (33,    'dccp'),
    (36,    'xtp'),
    (37,    'ddp'),
    (38,    'idpr-cmtp'),
    (41,    'ipv6'),
    (43,    'ipv6-route'),
    (44,    'ipv6-frag'),
    (45,    'idrp'),
    (46,    'rsvp'),
    (47,    'gre'),
    (50,    'esp'),
    (51,    'ah'),
    (57,    'skip'),
    (58,    'ipv6-icmp'),
    (59,    'ipv6-nonxt'),
    (60,    'ipv6-opts'),
    (73,    'rspf'),
    (81,    'vmtp'),
    (88,    'eigrp'),
    (89,    'ospf'),
    (93,    'ax.25'),
    (94,    'ipip'),
    (97,    'etherip'),
    (98,    'encap'),
    (103,  'pim'),
    (108,  'ipcomp'),
    (112,  'vrrp'),
    (115,  'l2tp'),
    (124,  'isis'),
    (132,  'sctp'),
    (133,  'fc'),
    (136,  'udplite'),
    (137,  'mpls-in-ip'),
    (138,  'manet'),
    (139,  'hip'),
    (140,  'shim6'),
    (141,  'wesp'),
    (142,  'rohc'),
)


class Traffic(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    logday = models.DateField(verbose_name='Log Day')
    srcip = models.IPAddressField(verbose_name='Source IP')
    dstip = models.IPAddressField(verbose_name='Destination IP')
    ip_protocol = models.IntegerField(choices=PROTOCOL_CHOICES, verbose_name='Protocol')
    port = models.IntegerField(db_column='l4_dport', verbose_name='Port')
    raw_in_pktlen = models.BigIntegerField(verbose_name='Bytes In')
    raw_in_pktcount = models.BigIntegerField(verbose_name='Packets In')
    raw_out_pktlen = models.BigIntegerField(verbose_name='Bytes Out')
    raw_out_pktcount = models.BigIntegerField(verbose_name='Packets Out')
    flow_duration = models.IntegerField(verbose_name='Flow Duration')
    flow_count = models.BigIntegerField(verbose_name='Flow Count')

    def srcnet(self):
        return str('Source Net')

    def dstnet(self):
        return str('Dest Net')

    def __unicode__(self):
        return "%s: %s %s" % (self.logday, self.srcip, self.dstip)

    class Meta:
        db_table = u'accounting'
        managed = False
        verbose_name_plural = u'traffic'

ordering = ['-logday']


class Authorization(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    logday = models.DateField(verbose_name='Log Day')
    logtime = models.DateTimeField(verbose_name='Timestamp')
    srcip = models.IPAddressField(verbose_name='Source IP')
    username = models.CharField(max_length=20)
    facility = models.CharField(max_length=20)
    authresult = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s %s" % (self.logtime, self.username)

    @models.permalink
    def get_absolute_url(self):
        return ('login_detail', (), {'username': self.username})

    class Meta:
        db_table = u'auth'
        managed = False


class Intrusion(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    logday = models.DateField()
    srcip = models.IPAddressField(verbose_name='Source IP')
    dstip = models.IPAddressField(verbose_name='Destination IP')
    groupid = models.IntegerField()
    ruleid = models.IntegerField()
    alert_packets = models.BigIntegerField()
    drop_packets = models.BigIntegerField()

    def __unicode__(self):
        return "%s: %s %s" % (self.logday, self.srcip, self.dstip)

    class Meta:
        db_table = u'ips'
        managed = False


class IntrusionCount(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    groupid = models.IntegerField()
    ruleid = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        db_table = u'ipscount'
        managed = False


class PacketFilter(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    logday = models.DateField()
    srcip = models.IPAddressField()
    dstip = models.IPAddressField()
    svc = models.CharField(max_length=20, verbose_name='service')
    packets = models.BigIntegerField()

    def __unicode__(self):
        return "%s: %s %s" % (self.logday, self.srcip, self.dstip)

    class Meta:
        db_table = u'pfilter'
        managed = False


class VpnConnection(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='_rowno')
    logday = models.DateField()
    logintime = models.DateTimeField()
    logouttime = models.DateTimeField()
    status = models.IntegerField()
    username = models.CharField(max_length=20)
    service = models.CharField(max_length=20)
    src_ip = models.IPAddressField(verbose_name='Source IP')
    virt_ip = models.IPAddressField(verbose_name='Virtual IP')
    pktlen_in = models.BigIntegerField()
    pktlen_out = models.BigIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.logintime, self.username)

    class Meta:
        db_table = u'vpn'
        managed = False


class CalculatedTraffic(models.Model):
    logday = models.DateField()
    srcip = models.IPAddressField()
    srcnet = models.CharField(max_length=20)
    dstip = models.IPAddressField()
    dstnet = models.CharField(max_length=20)
    traffic_in = models.BigIntegerField()
    traffic_out = models.BigIntegerField()

    def __unicode__(self):
        return "%s: %s %s" % (self.logday, self.srcip, self.dstip)

    class Meta:
        db_table = u'calctraffic'
        managed = False
