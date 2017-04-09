from django.contrib import admin
from django_iot.apps.devices.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_type', 'location')
    list_filter = ('device_type', 'location')


admin.site.register(Device, DeviceAdmin)
