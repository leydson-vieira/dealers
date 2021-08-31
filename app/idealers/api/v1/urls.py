from django.urls import path

from .views import cashback_view, dealer_view, order_view

urlpatterns = [
    path('dealers/', dealer_view, name='dealers'),
    path('orders/', order_view, name='orders'),
    path('orders/<uuid:order_id>/', order_view, name='orders-detail'),
    path('cashback/', cashback_view, name='accumulated-cashback'),
]
