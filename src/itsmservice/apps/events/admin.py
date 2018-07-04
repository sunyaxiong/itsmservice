from django.contrib import admin

from .models import Event
from .models import EventProcessLog


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "technician", "event_type", "app_name", "dt_created")
    list_filter = ("state", "event_type")


class EventLogAdmin(admin.ModelAdmin):
    list_display = ("event_obj", "username", "content", "dt_created")


admin.site.register(Event, EventAdmin)
admin.site.register(EventProcessLog, EventLogAdmin)