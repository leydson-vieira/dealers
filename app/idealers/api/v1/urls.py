from django.urls import path

from .views import dealer_view, order_view


urlpatterns = [
    path('dealers/', dealer_view, name='dealers'),
    path('orders/', order_view, name='orders'),
]