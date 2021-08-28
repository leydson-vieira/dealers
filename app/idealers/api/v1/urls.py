from django.urls import path

from .views import dealer_view


urlpatterns = [
    path('dealers/', dealer_view),
]