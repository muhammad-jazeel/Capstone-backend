from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', category_list, name='category-list'),
    path('categories/add/', category_add, name='category-create'),
]