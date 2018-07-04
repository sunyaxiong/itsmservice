from django.contrib import admin

from .models import Issue


class IssueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Issue, IssueAdmin)

