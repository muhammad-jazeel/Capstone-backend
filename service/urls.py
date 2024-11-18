from django.urls import path
from .views import *

urlpatterns = [
    path('services/', services_view, name='services'),
    path('add_service_view/', add_services_view, name='add_services_view')
]