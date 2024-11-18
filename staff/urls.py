from django.urls import path
from .views import *

urlpatterns = [
    # path('staffs/add/', views.add_staff_view, name='add_staff_view'),
    # path('staffs/edit/<int:pk>/', views.edit_staff_view, name='edit_staff_view'),
    # path('staffs/delete/<int:pk>/', views.delete_staff_view, name='delete_staff_view'),
    path('staff', staffs_view, name='staffs'),
    path('addstaff/', add_staff_view, name='add_staff'),
    # path('edit/<int:staff_id>/', edit_staff_view, name='edit_staff'),
    path('editstaff/', edit_staff_view, name='edit_staff'),
    # path('delete/<int:staff_id>/', delete_staff_view, name='delete_staff'),
    path('deletestaff/', delete_staff_view, name='delete_staff'),
]
