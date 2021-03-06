from django.contrib import admin

from .models import Profile
from .models import Department
from .models import Channel
from .models import MessageAlert
from .models import JobTitle


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "email", "department")
    search_fields = ("department__org__name", )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "org")


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", )


class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "_org_name")

    def _org_name(self, intance):
        return intance.department.org.name


class MessageAlertAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "action_type")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(MessageAlert, MessageAlertAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
