from .models import *
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Board
        fields = ['title', 'visibility', 'description', 'members']

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'visibility', 'description']