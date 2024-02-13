# Import the path function from django.urls module.
# This function is used to define individual URL patterns.
from django.urls import path

# Import TokenObtainPairView and TokenRefreshView from rest_framework_simplejwt.views.
# TokenObtainPairView is used to obtain a JWT token pair (access and refresh tokens) for authenticated users.
# TokenRefreshView is used to obtain a new access token using a non-expired refresh token.
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

# Import the views module from the current application.
# This module contains the view functions or classes that handle requests for different URL patterns.
from . import views

# Define a list named urlpatterns.
# This list contains the mapping between URL path expressions to the view functions or classes that should handle them.
urlpatterns = [
    # Define a URL pattern for user signup.
    # When the 'user/signup/' URL is accessed, the user_register view from the views module will be invoked.
    # 'name' is used to refer to this URL pattern in templates and view functions.
    path('user/signup/', views.user_register, name='user_signup'),

    # Define a URL pattern for user login to obtain JWT token pair.
    # TokenObtainPairView.as_view() creates an instance of the view to handle the request.
    # This URL is named 'token_obtain_pair', allowing it to be referred to easily elsewhere.
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Define a URL pattern for refreshing JWT access tokens.
    # TokenRefreshView.as_view() is used here to provide a new access token given a valid refresh token.
    # The URL is named 'token_refresh' for easy reference.
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Define a URL pattern for accessing the user profile.
    # UserProfileView is a class-based view defined in the views module, wrapped with as_view() to handle the request.
    # The URL pattern is named 'user-profile' for convenient referencing in templates and view functions.
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile')
]
