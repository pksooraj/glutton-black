from django.urls import path
from . import views

app_name = 'shop_orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]