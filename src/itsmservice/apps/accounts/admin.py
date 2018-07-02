from django.contrib import admin

from .models import Profile
from .models import Channel
from .models import MessageAlert


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "email", "department")


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", )


class MessageAlertAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "action_type")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(MessageAlert, MessageAlertAdmin)
