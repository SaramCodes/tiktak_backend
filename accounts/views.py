from rest_framework import generics
from rest_framework.views import APIView
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny 
from rest_framework.exceptions import ValidationError
from .serializers import UserCreateSerializer, UserUpdateSerializer, ProfileSerializer, CustomTokenObtainPairSerializer, UserRetrieveSerializer, UserFollowingSerializer, UserFollowersSerializer
from rest_framework.parsers import MultiPartParser 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()   
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]     
    parser_classes = [MultiPartParser]   
     
    def perform_update(self, serializer):
        user = User.objects.get(pk=self.kwargs['pk'])
        if not self.request.user == user:
            raise ValidationError("You don't have permission to edit this profile!", code=500)
        instance = serializer.save() 
        profile = instance.profile
        print(self.request.FILES)
        if self.request.FILES:
            profile.image = self.request.FILES['image']
        else:
            pass
        profile.description = self.request.POST['description']
        profile.save()

class UserImageUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        user = User.objects.get(pk=self.kwargs['pk'])
        if not self.request.user == user:
            raise ValidationError("You don't have permission to edit this profile!", code=500)
        serializer.save()

class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [AllowAny] 

class UserFollowersRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowersSerializer
    permission_classes = [AllowAny] 

class UserFollowingRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = [AllowAny] 

class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user = User.objects.get(pk=pk)
        print(user.profile.followers.filter(pk=request.user.pk).exists())

        if user.profile.followers.filter(pk=request.user.pk).exists():
            return Response({"error": "Already following this user!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.profile.followers.add(request.user)
            user.save()
            r_user = request.user
            r_user.profile.following.add(user)
            r_user.save()
            return Response("Followed successfully!",status=status.HTTP_201_CREATED)


class UserUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if user.profile.followers.filter(pk=request.user.pk).exists():
            user.profile.followers.remove(request.user)
            user.save()
            r_user = request.user
            r_user.profile.following.remove(user)
            r_user.save()
            return Response("Unfollowed successfully!",status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User wasn't followed to begin with!"}, status=status.HTTP_400_BAD_REQUEST)


