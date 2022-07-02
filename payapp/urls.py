from django.urls import path, include
from .views import index, accountant_creation, login_user

app_name="payapp"

urlpatterns = [
    path('', index, name='index'),
    path('accountant/create/',accountant_creation, name='accoutant_create'),
    path('login/',login_user, name='login'),


    # login_user
]
