from django.shortcuts import render
from .serializers import PostListCreateSerializer, PostDetailSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework import generics
from .models import Post
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from rest_framework.exceptions import ValidationError

"""This API will return all the posts but will not not return the actual
 comments and list of people who liked, it will only return the count. This API
 is also responsible for creating a POST"""
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

"""This API will return a single Post"""
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    
"""This API will create a Comment for a Post"""
class CommentCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = User.objects.get(pk=serializer.validated_data['user'].pk)
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
        except:
            raise ValidationError("Post matching the query doesn't exist", code=500)
        if not self.request.user == user:
            raise ValidationError("You have to login to post a comment!", code=500)
        serializer.save(user=user, post=post)    