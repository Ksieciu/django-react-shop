from django.urls import path
from .views import add_order_items, get_order_by_id, update_order_payment_status


urlpatterns = [
    path('add/', add_order_items, name='add-order'),
    path('<int:pk>/', get_order_by_id, name='get-order'),
    path('<int:pk>/pay/', update_order_payment_status, name='pay-order'),
]