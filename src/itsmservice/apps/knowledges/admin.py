from django.contrib import admin

from .models import Knowledge


class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ("title", "state", "creater")


admin.site.register(Knowledge, KnowledgeAdmin)
