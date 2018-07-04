from django import forms
from django.forms import ValidationError

from apps.changes.models import Change


class IssueDetailForm(forms.Form):

    emergency_degree = forms.ChoiceField(choices=Change.EMERGENCY_DEGREE)
    solution = forms.CharField(required=False)
    handler = forms.CharField()
    attach_file = forms.FileField(required=False)
    description = forms.CharField(required=False)

    def clean_handler(self):
        if self.data.get("handler") == "None":
            raise ValidationError("请指派处理人")


class IssueToKnowForm(forms.Form):

    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    attach_file = forms.FileField()
    issue_id = forms.IntegerField(required=False)
    issue_name = forms.CharField(required=False)
    classify = forms.CharField(required=False)