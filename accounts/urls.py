from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from . import views

urlpatterns = [
    path('user/signup/', views.user_register, name='user_signup'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile')
]