from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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
        fields = ['image', 'description']


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
