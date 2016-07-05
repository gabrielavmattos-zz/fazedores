from django import forms

class FormAlgoritmo(forms.Form):
    algoritmo = forms.CharField(
        required=True,
        widget=forms.Textarea,
        initial="comando_setup\n   ativar(som, 5)\nfim_comando_setup\n\ncomando_loop\n   ligar(som, 5)\n   esperar(1)\n   desligar(som, 5)\n   esperar(1)\nfim_comando_loop"
    )
