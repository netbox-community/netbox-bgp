from django.contrib import admin
from .models import ASN, Community, BGPSession


@admin.register(ASN)
class ASNAdmin(admin.ModelAdmin):
    fields = ('number', 'name', 'status', 'description')


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    fields = ('value', 'name', 'status', 'description')


@admin.register(BGPSession)
class BGPSessionAdmin(admin.ModelAdmin):
    fields = ('local_address', 'local_as', 'remote_address', 'remote_as' 'description')
