from rest_framework import generics
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny 
from rest_framework.exceptions import ValidationError
from .serializers import UserCreateSerializer, UserUpdateSerializer
from rest_framework.parsers import MultiPartParser 


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()   
    serializer_class = UserUpdateSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]     
    parser_classes = [MultiPartParser]    
    def perform_update(self, serializer):
        instance = serializer.save() 
        profile = instance.profile
        print(self.request.FILES)
        if self.request.FILES:
            profile.image = self.request.FILES['image']
        else:
            pass
        profile.description = self.request.POST['description']
        profile.save()
