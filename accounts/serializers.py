# Import serializers from the Django REST Framework (DRF).
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML, or other content types. They also provide deserialization,
# allowing parsed data to be converted back into complex types, after first validating the incoming data.
from rest_framework import serializers

# Import TokenObtainPairSerializer from the rest_framework_simplejwt.serializers module.
# This serializer is used for obtaining a JWT token pair (access and refresh tokens) for a given user.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import the User model from the current application's models.
# This model definition is used to interact with the User data in the database.
from .models import User

# Define a serializer class for obtaining JWT token pair with possible customization.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Generate a token for a given user by calling the superclass's method and passing the user object.
        # This allows for any customization or additional data to be added to the token if necessary.
        token = super().get_token(user)
        
        # Return the token. Custom claims can be added here if needed.
        return token

# Define a serializer for the User model for standard operations such as retrieval.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the User model that this serializer will serialize/deserialize.
        model = User
        # Define the fields that should be included in the serialized output, or are accepted in deserialization.
        fields = ['username', 'email', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']

# Define a serializer for user registration.
class UserRegistrationSerializer(serializers.ModelSerializer):
    # Define a password field that is write-only. This means it will be accepted on input,
    # typically for user creation or updating, but will not be included in the serialized output.
    password = serializers.CharField(write_only=True)
    
    class Meta:
        # Specify the User model to serialize/deserialize.
        model = User
        # Define the fields that this serializer will accept or include in its output.
        # Note that 'password' is write-only, so it won't be included in the serialized representation.
        fields = ['username', 'email', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']
