from django import forms

from candidate.models import Activity


class ActivityForm(forms.Form):
    name = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        label="",
        widget=forms.CheckboxSelectMultiple,
    )
