from django.urls import path, include
from .views import get_product, get_products_list, MyTokenObtainPairView, get_current_user


urlpatterns = [
    path('users/login/', MyTokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('users/profile/', get_current_user, name='user_profile'),
    path('products/', get_products_list),
    path('product/<str:pk>', get_product),
]
