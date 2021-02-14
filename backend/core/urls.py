from django.urls import path, include
from .views import (get_product, get_products_list)


urlpatterns = [
    path('', get_products_list),
    path('<str:pk>', get_product),
]
