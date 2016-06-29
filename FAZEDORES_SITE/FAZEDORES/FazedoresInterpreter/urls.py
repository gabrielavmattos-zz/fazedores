from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.exibe_programas),
    url(r'^exibe_programas/$', views.algoritmo),
]
