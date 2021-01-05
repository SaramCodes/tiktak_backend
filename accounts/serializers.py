from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from feed.models import Post

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_image'] = user.profile.image.url
        return token

        
class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password": "Passwords fields don't match!"})

        return attr

    def create(self, validated_data):
        try:
            first_name = validated_data['first_name']
        except:
            first_name = ""
        try:
            last_name = validated_data['last_name']
        except:
            last_name = ""
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    description = serializers.CharField(source="profile.description")
    image = serializers.ImageField(required=False, source="profile.image")
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'description', 'image']
 
    def update(self, instance, validated_data):
        if validated_data['username'] != instance.username:
            if User.objects.filter(username=validated_data['username']).exists():
                raise serializers.ValidationError({"username": "username taken"})
        if validated_data['email'] != instance.email:
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError({"email": "email already exists"})
        try:
            instance.first_name = validated_data['first_name']
        except:
            pass
        try:
            instance.last_name = validated_data['last_name']
        except:
            pass
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()

        # if validated_data['profile']['image'] != instance.profile.image:
        # instance =super().update(instance, validated_data)
        return instance    



class UserSubFollowingSerializer(serializers.ModelSerializer):    
    image = serializers.ImageField(use_url=True, source="profile.image")
    class Meta:
        model = User
        fields = ['id', 'username', 'image']

class UserFollowersSerializer(serializers.ModelSerializer):    
    users = UserSubFollowingSerializer(many=True, source="profile.followers.all")
    class Meta:
        model = User
        fields = ['users']

class UserFollowingSerializer(serializers.ModelSerializer):    
    users = UserSubFollowingSerializer(many=True, source="profile.following.all")
    class Meta:
        model = User
        fields = ['users']

class UserPostsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'video']

class UserRetrieveSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(source="profile.followers.count")
    following = serializers.IntegerField(source="profile.following.count")
    image = serializers.ImageField(source="profile.image")
    description = serializers.CharField(source="profile.description")
    posts = UserPostsSerialzer(source='post_set.all', many=True)
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'image', 'description', 'followers', 'following', 'posts']

