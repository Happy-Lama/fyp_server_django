from django.urls import path
from . import views

urlpatterns = [
    path('data/gsm/', views.gsm_receive_data, name='gsm_receive'),
    path('data/ttn/', views.ttn_receive_data, name='ttn_receive'),
]
