from django.contrib import admin

from .models import Config


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name", "state", "event_module", "issue_module", "change_module", "sla_module"
    )


admin.site.register(Config, ConfigAdmin)
