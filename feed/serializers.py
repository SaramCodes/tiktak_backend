from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="id")
    user_image = serializers.ImageField(use_url=True, source="profile.image")
    class Meta:
        model = User
        fields = ['user', 'username', 'user_image']

class PostListCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = serializers.IntegerField(source='comment_set.all.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id','title', 'video', 'user', 'likes', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_image = serializers.ImageField(use_url=True, source="user.profile.image", read_only=True)
    class Meta:
        model = Comment
        fields = ['user', 'username', 'user_image', 'content']



class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source="comment_set.all")
    likes = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'video', 'user', 'likes', 'comments']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'content']