from django.shortcuts import render
from django.http import HttpResponse
from .models import Algoritmo
from .forms import FormAlgoritmo
from .Interpreter import Interpreter
import string


def exibe_programas(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'FazedoresInterpreter/index.html')

def algoritmo(request):
    form_class = FormAlgoritmo()
    if request.method == 'POST': 
        form_class = FormAlgoritmo(request.POST)
        if form_class.is_valid(): 
            #alg = form_class.cleaned_data['algoritmo']
            #print ("1 "+form_class['algoritmo'].value())
            #print ("2 "+form_class.data['algoritmo']) 
            #alg=form_class['algoritmo'].value()
            alg=request.POST.get('algoritmo')
            print(alg)
            algoritmo = str(alg)
            print("Convertido para string \n\n"+algoritmo)
            interpretador = Interpreter(algoritmo)
            algoritmo_interpretado = interpretador.startInterpreter()
	    resposta = ""
            if(algoritmo_interpretado == False):
                resposta = interpretador.msgError
            else:    
                resposta = algoritmo_interpretado[1]
            print(resposta)
            return render(request, 'FazedoresInterpreter/algoritmo.html', {'form': form_class, 'algoritmo': resposta}) # Redirect after POST   
        else:
            form_class = FormAlgoritmo()    
    
    
    return render(request, 'FazedoresInterpreter/algoritmo.html', {
        'form': form_class,
    })    
