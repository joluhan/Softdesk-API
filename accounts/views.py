from datetime import date
from accounts.models import User
from rest_framework.response import Response
from accounts.serializers import MyTokenObtainPairSerializer, UserRegistrationSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.generics import RetrieveUpdateDestroyAPIView


# Create your views here.
@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if 'date_of_birth' in serializer.validated_data:
                print("afetr  ",  request.data)
                birthdate = serializer.validated_data['date_of_birth']
                age = date.today().year - birthdate.year
                
                if age > 15:
                    password = make_password(serializer.validated_data['password'])
                    serializer.validated_data['password'] = password
                    user = serializer.save()
                    token = MyTokenObtainPairSerializer.get_token(user)
                    
                    return Response({
                            'access': str(token.access_token),
                            'refresh': str(token),
                            'message': 'User registered successfully'
                        }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                                'message': 'You must be at least 15 years old to register.'
                            }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                        'message': 'The date of birth is required.'
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get User Profile
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Update User Profile
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Delete User profile
        user = self.request.user
        user.delete()
        return Response({'message': 'Compte utilisateur supprimé avec succès'},
                        status=status.HTTP_204_NO_CONTENT)
