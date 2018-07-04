from django import forms
from django.forms import ValidationError

from .models import Change


class ChangeDetailForm(forms.Form):

    emergency_degree = forms.CharField(required=False)
    solution = forms.CharField(required=False)
    node_handler = forms.CharField()
    attach_file = forms.FileField(required=False)
    description = forms.CharField(required=False)


class ChangeDetailModelForm(forms.ModelForm):

    description = forms.Textarea(attrs={"class": "type"})

    class Meta:
        model = Change
        fields = "__all__"
