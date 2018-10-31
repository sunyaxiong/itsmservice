from django.contrib import admin

from .models import Event, Classify
from .models import EventProcessLog
from .models import EventAttachments


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "handler", "classify", "dt_created")
    list_filter = ("state", "classify")


class EventLogAdmin(admin.ModelAdmin):
    list_display = ("event_obj", "user", "content", "dt_created")


class RequestClassifyAdmin(admin.ModelAdmin):
    list_display = ("value", "level")


class EventAttachmentsAdmin(admin.ModelAdmin):
    list_display = ("event", "upload_user")

admin.site.register(Classify, RequestClassifyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventProcessLog, EventLogAdmin)
admin.site.register(EventAttachments, EventAttachmentsAdmin)