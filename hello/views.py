from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import re
import requests
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from hello.forms import PropiedadForm
from .models import PredictionHistory 
from django.http import JsonResponse
from django.shortcuts import render

# Configuración del endpoint de Databricks
DATABRICKS_ENDPOINT = "https://adb-3987092476296021.1.azuredatabricks.net/serving-endpoints/EP_APP_SERVICE/invocations"
DATABRICKS_TOKEN = "dapia7c0084a56d59e00268ff7b99eb0cf8f-2"

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

    return render(request, 'hello/model_idealista.html', {'form': form, 'propiedad_creada': propiedad_creada})

def predict_view(request):
    # Valores predeterminados para el formulario
    bathrooms = 1
    isparking = 0
    latitude = 40.4167
    longitude = -3.70325
    rooms = 2
    size = 50
    year = 2024
    quarter = 1
    predictions = None

    if request.method == "POST":
        # Leer los valores del formulario (en el caso de POST)
        bathrooms = float(request.POST.get("bathrooms", bathrooms))
        isparking = float(request.POST.get("isparking", isparking))
        latitude = float(request.POST.get("latitude", latitude))
        longitude = float(request.POST.get("longitude", longitude))
        rooms = float(request.POST.get("rooms", rooms))
        size = float(request.POST.get("size", size))
        year = float(request.POST.get("year", year))
        quarter = float(request.POST.get("quarter", quarter))

        # Crear el vector de características
        features = [bathrooms, isparking, latitude, longitude, rooms, size, year, quarter]

        # Crear el payload
        payload = {
            "dataframe_records": [
                {"features": features}
            ]
        }

        # Hacer la solicitud al endpoint
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(DATABRICKS_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            predictions = response.json()  # Obtener la respuesta JSON

            # Asignar el valor de la predicción o un valor predeterminado
            prediction_value = predictions["predictions"][0] if "predictions" in predictions else 0

            # Guardar en la base de datos el historial de predicciones
            PredictionHistory.objects.create(
                bathrooms=bathrooms,
                isparking=isparking,
                latitude=latitude,
                longitude=longitude,
                rooms=rooms,
                size=size,
                year=year,
                quarter=quarter,
                prediction_value=prediction_value  # El valor de la predicción
            )
        else:
            predictions = f"Error {response.status_code}: {response.text}"

    # Pasamos los valores al formulario (en el caso de GET o POST)
    prediction_history = PredictionHistory.objects.all().order_by("-log_date")[:5]  # Últimas 5 predicciones
    return render(request, "hello/predictions.html", {
        "bathrooms": bathrooms,
        "isparking": isparking,
        "latitude": latitude,
        "longitude": longitude,
        "rooms": rooms,
        "size": size,
        "year": year,
        "quarter": quarter,
        "predictions": predictions,  # Aseguramos que esta variable esté disponible
        "prediction_history": prediction_history
    })


"""
def predict_view(request):
    predictions = None
    if request.method == "POST":
        # Leer valores del formulario
        bathrooms = float(request.POST.get("bathrooms", 1))
        isparking = float(request.POST.get("isparking", 0))
        latitude = float(request.POST.get("latitude", 40.4167))
        longitude = float(request.POST.get("longitude", -3.70325))
        rooms = float(request.POST.get("rooms", 2))
        size = float(request.POST.get("size", 50))
        year = float(request.POST.get("year", 2024))
        quarter = float(request.POST.get("quarter", 1))

        # Crear el vector de características
        features = [bathrooms, isparking, latitude, longitude, rooms, size, year, quarter]

        # Crear el payload
        payload = {
            "dataframe_records": [
                {"features": features}
            ]
        }

        # Hacer la solicitud al endpoint
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(DATABRICKS_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            predictions = response.json()  # Obtener la respuesta JSON

            if "predictions" in predictions:
                predictions = predictions["predictions"][0]  # Tomar la primera predicción
                prediction_value = predictions  # El precio predicho

                # Guardar en la base de datos el historial de predicciones
                PredictionHistory.objects.create(
                    bathrooms=bathrooms,
                    isparking=isparking,
                    latitude=latitude,
                    longitude=longitude,
                    rooms=rooms,
                    size=size,
                    year=year,
                    quarter=quarter,
                    prediction_value=prediction_value  # Guardamos la predicción
                )
            else:
                predictions = "No predictions field in response"
        else:
            predictions = f"Error {response.status_code}: {response.text}"

    # Pasamos el historial de predicciones a la plantilla
    prediction_history = PredictionHistory.objects.all().order_by("-log_date")[:5]  # Últimas 5 predicciones
    return render(request, "hello/predictions.html", {
        "predictions": predictions,
        "prediction_history": prediction_history
    })
"""

"""
def predict_view(request):
    predictions = None
    prediction_history = PredictionHistory.objects.all().order_by("-log_date")[:5]  # Obtiene las últimas 5 predicciones
    if request.method == "POST":
        # Leer valores del formulario y convertirlos
        bathrooms = float(request.POST.get("bathrooms", 1))
        isparking = float(request.POST.get("isparking", 0))
        latitude = float(request.POST.get("latitude", 40.4167))
        longitude = float(request.POST.get("longitude", -3.70325))
        rooms = float(request.POST.get("rooms", 2))
        size = float(request.POST.get("size", 50))
        year = float(request.POST.get("year", 2024))
        quarter = float(request.POST.get("quarter", 1))

        # Crear el vector de características
        features = [bathrooms, isparking, latitude, longitude, rooms, size, year, quarter]

        # Crear el payload
        payload = {
            "dataframe_records": [
                {"features": features}
            ]
        }

        # Hacer la solicitud al endpoint
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(DATABRICKS_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            predictions = response.json()  # Obtener la respuesta JSON

            if "predictions" in predictions:
                predictions = predictions["predictions"][0]  # Tomar la primera predicción
                prediction_value = predictions  # El precio predicho

                # Guardar en la base de datos el historial de predicciones
                PredictionHistory.objects.create(
                    bathrooms=bathrooms,
                    isparking=isparking,
                    latitude=latitude,
                    longitude=longitude,
                    rooms=rooms,
                    size=size,
                    year=year,
                    quarter=quarter,
                    prediction_value=prediction_value
                )
            else:
                predictions = "No predictions field in response"
        else:
            predictions = f"Error {response.status_code}: {response.text}"

    return render(request, "hello/predictions.html", {
        "predictions": predictions,
        "prediction_history": prediction_history  # Pasamos el historial a la plantilla
    })

"""

