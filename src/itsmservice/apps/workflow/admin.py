from django.contrib import admin

from .models import FlowNode, FlowModule


class FlowNodeAdmin(admin.ModelAdmin):

    list_display = (
        "name", "number", "job_title", "flow_module", "_org_name"
    )

    def _org_name(self, instance):
        return instance.job_title.department.org.name


class FlowModuleAdmin(admin.ModelAdmin):

    list_display = ("name", "org", "creator")


admin.site.register(FlowModule, FlowModuleAdmin)
admin.site.register(FlowNode, FlowNodeAdmin)
