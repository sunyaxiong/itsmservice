from django import forms
from django.forms import ValidationError

from .models import Event


class EventDetailForm(forms.Form):

    emergency_degree = forms.ChoiceField(required=False)
    solution = forms.CharField(required=False)
    technician = forms.CharField(required=False)
    attach_file = forms.FileField(required=False)

    def clean_technician(self):
        if self.data.get("technician") == "None":
            raise ValidationError("请指派处理人")


class EventDetailModelForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-group"}), label="事件名称"
    )
    description = forms.CharField(
        widget=forms.Select(attrs={"class": "form-control"}), label="事件描述"
    )

    class Meta:
        model = Event
        fields = "__all__"