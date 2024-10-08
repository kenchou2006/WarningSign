from django.contrib import admin
from .models import AccessRecord

class AccessRecordAdmin(admin.ModelAdmin):
    list_display = ('access_time', 'ip_address','urls' ,'os_name', 'browser_name')
    search_fields = ['ip_address', 'os_name', 'browser_name']
    list_filter = ['access_time']

admin.site.register(AccessRecord, AccessRecordAdmin)
