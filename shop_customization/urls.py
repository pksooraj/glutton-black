from django.urls import path
from . import views

app_name = 'customization'

urlpatterns = [
    path('', views.customize, name='customize'),
    path('add-to-cart/', views.add_custom_to_cart, name='add_custom_to_cart'),
]