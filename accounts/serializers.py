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