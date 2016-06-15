from django.shortcuts import render
from django.http import HttpResponse
from .models import Algoritmo
from .forms import FormAlgoritmo
from .Interpretador import Interpretador


def exibe_programas(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'FazedoresInterpreter/index.html')

def algoritmo(request):
    form_class = FormAlgoritmo()
    if request.method == 'POST': 
        form_class = FormAlgoritmo(request.POST)
        if form_class.is_valid(): 
            algoritmo = form_class.cleaned_data['content']
            algoritmo="Algoritmo"
            #interpretador = Interpretador(algoritmo)
            #algoritmo_interpretado = interpretador.interpreta()
            return render(request, 'FazedoresInterpreter/algoritmo.html', {'form': form_class, 'algoritmo': algoritmo}) # Redirect after POST   
        else:
            form_class = FormAlgoritmo()    
    
    
    return render(request, 'FazedoresInterpreter/algoritmo.html', {
        'form': form_class,
    })    

def resultado(request):
    return render(request, 'FazedoresInterpreter/resultado.html')

