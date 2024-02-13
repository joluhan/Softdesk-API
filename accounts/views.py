# Import the date class from the datetime module to work with dates.
from datetime import date

# Import the User model from the accounts application's models.
from accounts.models import User

# Import the Response class from the rest_framework.response module.
# Response objects are used to return data from API views.
from rest_framework.response import Response

# Import serializer classes from the accounts application's serializers.
# These serializers convert complex data types to and from Python native datatypes for rendering into JSON or other content types.
from accounts.serializers import MyTokenObtainPairSerializer, UserRegistrationSerializer, UserSerializer

# Import the api_view decorator from rest_framework.decorators.
# This decorator is used to specify the allowed HTTP methods for a view function.
from rest_framework.decorators import api_view

# Import IsAuthenticated from rest_framework.permissions.
# IsAuthenticated is a permission class that allows access to authenticated users only.
from rest_framework.permissions import IsAuthenticated

# Import the status module from rest_framework.
# This module provides status codes for HTTP responses.
from rest_framework import status

# Import the make_password function from django.contrib.auth.hashers.
# make_password is used for hashing passwords.
from django.contrib.auth.hashers import make_password

# Import RetrieveUpdateDestroyAPIView from rest_framework.generics.
# This class provides a generic view for retrieving, updating, or deleting an object.
from rest_framework.generics import RetrieveUpdateDestroyAPIView


@api_view(['POST'])
def user_register(request):
    # Check if the request method is POST.
    if request.method == 'POST':
        # Deserialize the request data using the UserRegistrationSerializer.
        serializer = UserRegistrationSerializer(data=request.data)
        # Check if the deserialized data is valid.
        if serializer.is_valid():
            # Check if date_of_birth and consent_to_data_stock are provided.
            if 'date_of_birth' in serializer.validated_data and 'consent_to_data_stock' in serializer.validated_data:
                # Extract the birthdate from the validated data.
                birthdate = serializer.validated_data['date_of_birth']
                # Calculate the age of the user based on the birthdate.
                age = date.today().year - birthdate.year
                # Check if the user's age is greater than 15 and consent is given.
                if age > 15 and serializer.validated_data['consent_to_data_stock']:
                    # Hash the password for security.
                    password = make_password(serializer.validated_data['password'])
                    # Replace the plain password with the hashed one.
                    serializer.validated_data['password'] = password
                    # Save the user to the database.
                    user = serializer.save()
                    # Generate a token for the user.
                    token = MyTokenObtainPairSerializer.get_token(user)
                    # Return a success response with access and refresh tokens.
                    return Response({
                            'access': str(token.access_token),
                            'refresh': str(token),
                            'message': 'User registered successfully'
                        }, status=status.HTTP_201_CREATED)
                else:
                    # Return an error if the user is under 15 or consent is not given.
                    error_message = "You must be at least 15 years old to register."
                    if not serializer.validated_data['consent_to_data_stock']:
                        error_message += " Consent to data stock is required."
                    return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Return an error if date_of_birth or consent_to_data_stock is missing.
                return Response({
                        'message': 'The date of birth and consent to data stock are required.'
                    }, status=status.HTTP_400_BAD_REQUEST)
        # Return error response if serializer validation fails.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define a class-based view for handling user profiles.
class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # Define the queryset that contains all users.
    serializer_class = UserSerializer  # Specify the serializer class to be used.
    permission_classes = [IsAuthenticated]  # Allow access to authenticated users only.

    def get(self, request, *args, **kwargs):
        # Handle GET requests to retrieve the user's profile.
        user = request.user  # Get the current user.
        serializer = self.get_serializer(user)  # Serialize the user's data.
        return Response(serializer.data)  # Return the serialized data.

    def update(self, request, *args, **kwargs):
        # Handle PUT/PATCH requests to update the user's profile.
        user = request.user  # Get the current user.
        serializer = UserSerializer(user, data=request.data, partial=True)  # Serialize the data with partial update support.
        if serializer.is_valid():
            serializer.save()  # Save the updated data.
            return Response(serializer.data)  # Return the updated data.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if validation fails.

    def delete(self, request, *args, **kwargs):
        # Handle DELETE requests to delete the user's profile.
        user = request.user  # Get the current user.
        user.delete()  # Delete the user.
        # Return a success message.
        return Response({'message': 'User profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
