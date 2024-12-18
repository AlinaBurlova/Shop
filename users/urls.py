from django.urls import path
from .views import (register, log_in, log_out, user_detail, change_password, change_profile)
# from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('log_in/', log_in, name='login'),
    path('log_out/', log_out, name='logout'),
    path('default/<int:pk>', user_detail, name='detail'),
    path('change_password/', change_password, name='change_password'),
    path('change_profile/', change_profile, name='change_profile'),
    # path('log_out/', LogoutView.as_view(next_page=""), name='logout'),
]