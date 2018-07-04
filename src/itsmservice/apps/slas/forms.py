from django import forms


class SatisfactionForm(forms.Form):

    # event = forms.CharField(required=False)
    sati_id = forms.IntegerField(required=True)
    comment = forms.CharField(required=True)
    content = forms.CharField(required=False)
    is_ended = forms.CharField(required=False)