from .models import *
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'visibility', 'description', 'members']

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'visibility', 'description']

class AddMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ['members']

    def validate(self, data):
        board = self.context['board']
        user = self.context['user']
        
        members = data.get('members')

        if user in members:
            raise serializers.ValidationError({'members':'Cannot add self.'})

        board.members.add(*members)
        return data

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title', 'position']


class ColumnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['title']

