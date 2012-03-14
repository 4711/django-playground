# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Accounting(models.Model):
    srcip = models.IPAddressField()
    dstip = models.IPAddressField()
    ip_protocol = models.IntegerField()
    l4_dport = models.IntegerField()
    raw_in_pktlen = models.BigIntegerField()
    raw_in_pktcount = models.BigIntegerField()
    raw_out_pktlen = models.BigIntegerField()
    raw_out_pktcount = models.BigIntegerField()
    logday = models.DateField()
    flow_duration = models.IntegerField()
    flow_count = models.BigIntegerField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'accounting'

class Ips(models.Model):
    logday = models.DateField()
    srcip = models.IPAddressField()
    dstip = models.IPAddressField()
    groupid = models.IntegerField()
    ruleid = models.IntegerField()
    alert_packets = models.BigIntegerField()
    drop_packets = models.BigIntegerField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'ips'

class Auth(models.Model):
    logtime = models.DateTimeField()
    logday = models.DateField()
    srcip = models.IPAddressField()
    username = models.TextField()
    facility = models.TextField()
    authresult = models.TextField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'auth'

class Ipscount(models.Model):
    groupid = models.IntegerField()
    ruleid = models.IntegerField()
    count = models.IntegerField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'ipscount'

class Pfilter(models.Model):
    logday = models.DateField()
    srcip = models.IPAddressField()
    dstip = models.IPAddressField()
    svc = models.TextField()
    packets = models.BigIntegerField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'pfilter'

class Vpn(models.Model):
    status = models.IntegerField()
    logintime = models.DateTimeField()
    logouttime = models.DateTimeField()
    logday = models.DateField()
    username = models.TextField()
    service = models.TextField()
    src_ip = models.IPAddressField()
    virt_ip = models.IPAddressField()
    pktlen_in = models.BigIntegerField()
    pktlen_out = models.BigIntegerField()
    _rowno = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'vpn'

class Calctraffic(models.Model):
    logday = models.DateField()
    srcip = models.IPAddressField()
    srcnet = models.CharField(max_length=-1)
    dstip = models.IPAddressField()
    dstnet = models.CharField(max_length=-1)
    mb_in = models.TextField()
    mb_out = models.TextField()
    class Meta:
        db_table = u'calctraffic'

