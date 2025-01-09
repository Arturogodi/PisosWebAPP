from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import re
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from hello.forms import PropiedadForm
from django.http import JsonResponse

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home(request):
    return render(request, "hello/home.html")

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("log_message")
    messages = LogMessage.objects.all().order_by("-log_date")
    
    return render(request, "hello/log_message.html", {"form": form, "messages": messages})
    #else:
    #    return render(request, "hello/log_message.html", {"form": form})

def model_idealista(request):
    propiedad_creada = None
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            metros = form.cleaned_data['metros']
            banos = form.cleaned_data['banos']
            estado = form.cleaned_data['estado']

            # Crea un diccionario con los datos ingresados para mostrarlo en la plantilla
            propiedad_creada = {
                'id': 1,  # O lo que sea tu ID identificador, puede ser generado dinámicamente
                'tipo': tipo,
                'metros': metros,
                'banos': banos,
                'estado': estado,
            }
    else:
        form = PropiedadForm()

    return render(request, 'hello/modelo_idealista.html', {'form': form, 'propiedad_creada': propiedad_creada})

""" 

def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return HttpResponse(content)
    """
