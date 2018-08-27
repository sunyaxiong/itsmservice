from django.contrib import admin

from .models import Event, Classify
from .models import EventProcessLog


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "handler", "classify", "dt_created")
    list_filter = ("state", "classify")


class EventLogAdmin(admin.ModelAdmin):
    list_display = ("event_obj", "username", "content", "dt_created")


class RequestClassifyAdmin(admin.ModelAdmin):
    list_display = ("value", "level")


admin.site.register(Classify, RequestClassifyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventProcessLog, EventLogAdmin)