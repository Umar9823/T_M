from django.urls import path
from .views import *

urlpatterns = [
    path('add-task/', add_task, name='add_task'),
    path('add-user/', add_user, name='add_user'),
    path('user-tasks/', user_tasks, name='user_tasks'),  # Add this line

    path('', dashboard, name='dashboard'),
    path('report/', report, name='report'),
]
