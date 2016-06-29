from django import forms

class FormAlgoritmo(forms.Form):
    algoritmo = forms.CharField(
        required=True,
        widget=forms.Textarea,
    )
