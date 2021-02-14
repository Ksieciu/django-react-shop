from django.urls import path, include
from .views import (MyTokenObtainPairView, get_current_user, 
                    get_users_list, register_user, update_user_profile)


urlpatterns = [
    path('', get_users_list, name='get_users'),
    path('register/', register_user, name='register_user'),
    path('login/', MyTokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('profile/', get_current_user, name='user_profile'),
    path('profile/update/', update_user_profile, name='user_profile_update'),
]