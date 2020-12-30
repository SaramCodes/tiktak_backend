from rest_framework import generics
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from rest_framework.exceptions import ValidationError
from .serializers import UserCreateSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # permission_classes = [IsAuthenticated]