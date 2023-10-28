from django.urls import path
from guitarguitar import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "guitarguitar"

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.view_orders, name='view_orders'),
    path('', views.view_customers, name='view_customers'),
    path('', views.view_products, name='view_products'),
]
