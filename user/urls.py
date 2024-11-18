from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user/<int:user_id>/', get_user, name='get-user'),
    path('get-all-users/', get_all_users, name='get-all-users'),
    # path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
