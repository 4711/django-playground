from django.contrib import admin
from models import *


class TrafficAdmin(admin.ModelAdmin):
    list_display = ('logday', 'srcip', 'dstip', 'port', 'ip_protocol', 'raw_in_pktlen', 'raw_out_pktlen')
    #ordering = ['-raw_in_pktlen', '-raw_out_pktlen', '-logday']
    list_per_page = 25
    search_fields = ['srcip', 'dstip']
    date_hierarchy = 'logday'
    list_filter = ('logday', )
    fieldsets = (
        ('Address', {'fields': (('srcip', 'dstip'), ('port', 'ip_protocol'))}),
        ('Traffic', {'fields': (('raw_in_pktcount', 'raw_in_pktlen'), ('raw_out_pktcount', 'raw_out_pktlen'))}),
        ('Flow', {'fields': (('flow_count', 'flow_duration'),)}),
    )


class AuthorizationAdmin(admin.ModelAdmin):
    list_display = ('logtime', 'username', 'facility', 'authresult')
    ordering = ['-logtime']
    list_per_page = 25
    search_fields = ['username']
    date_hierarchy = 'logday'
    list_filter = ('logday', )


class IntrusionAdmin(admin.ModelAdmin):
    list_display = ('logday', 'srcip', 'dstip', 'alert_packets', 'drop_packets')
    ordering = ['-logday']
    list_per_page = 25
    date_hierarchy = 'logday'
    list_filter = ('logday', )


class IntrusionCountAdmin(admin.ModelAdmin):
    list_display = ('groupid', 'ruleid', 'count')
    ordering = ['-count']
    list_per_page = 25
    list_filter = ('groupid', )


class PacketFilterAdmin(admin.ModelAdmin):
    list_display = ('logday', 'srcip', 'dstip', 'svc', 'packets')
    ordering = ['-logday']
    list_per_page = 25
    date_hierarchy = 'logday'
    list_filter = ('logday', )


class VpnConnectionAdmin(admin.ModelAdmin):
    list_display = ('logintime', 'username', 'service')
    ordering = ['-logintime']
    list_per_page = 25
    search_fields = ['username']
    date_hierarchy = 'logday'
    list_filter = ('logday', )

admin.site.register(VpnConnection, VpnConnectionAdmin)
admin.site.register(PacketFilter, PacketFilterAdmin)
admin.site.register(Traffic, TrafficAdmin)
admin.site.register(Authorization, AuthorizationAdmin)
admin.site.register(Intrusion, IntrusionAdmin)
admin.site.register(IntrusionCount, IntrusionCountAdmin)
