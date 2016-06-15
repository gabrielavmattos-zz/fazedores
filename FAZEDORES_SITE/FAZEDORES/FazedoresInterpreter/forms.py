from django import forms

class FormAlgoritmo(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
    )
