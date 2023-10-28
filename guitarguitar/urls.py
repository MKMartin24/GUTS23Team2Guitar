from django.urls import path
from guitarguitar import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "guitarguitar"

urlpatterns = [
    path('', views.index, name='index'),
]
