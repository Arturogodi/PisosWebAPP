from django.urls import path
from hello import views
from hello.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('log_message/', views.log_message, name='log_message'),
    path("log/", views.log_message, name="log"),
    path('model_idealista/', views.model_idealista, name='model_idealista'),
    path("predictions/", views.predict_view, name="predict"),
]

