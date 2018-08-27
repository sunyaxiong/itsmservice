from django.contrib import admin

from .models import Change
from .models import ChangeProcessLog


class ChangeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ("change", "username", "content")


admin.site.register(Change, ChangeAdmin)
admin.site.register(ChangeProcessLog, ChangeLogAdmin)