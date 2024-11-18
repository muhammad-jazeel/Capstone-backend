from django.urls import path
from .views import *

urlpatterns = [
    path('', departments_view, name='departments'),  
    path('add_department/', add_department_view, name='add_department'),  
    path('edit_department/', edit_department_view, name='edit_department'),  
    path('delete_department/', delete_department_view, name='delete_department'),  
]
