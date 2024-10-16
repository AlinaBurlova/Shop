from django.urls import path
from .views import (register, log_in, log_out)

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('log_in/', log_in, name='login'),
    path('log_out/', log_out, name='logout'),
]