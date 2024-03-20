from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('transformers/latest/', views.index, name='home'),
    path('transformers/register/', views.register_transformer),
    path('transformers/data/', views.get_overall_transformer_data),
    path('transformers/data/average/', views.moving_time_average_data),
    # path('get_csrf_token/', views.get_csrf_toke),
    # path('login/', views.login),
    # path('logout/', views.logout),
    path('transformers/<int:transformer_id>/', views.get_transformer_data),
    path('notifications/<str:filter>/', views.get_notifications),
    path('subscribe/<str:token>/', views.subscribe_to_notifications)
]
