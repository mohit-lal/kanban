from .models import *
from rest_framework import serializers

def parseDate(_date):
    return _date.strftime("%b %d, %Y %H:%M")

class DateSerializer(serializers.SerializerMethodField):
    def to_representation(self, value):
        _date = getattr(value, self.field_name)
        if _date:
            return parseDate(_date)
        return None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, data):

        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'username': 'Username already exists!'})

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'password':'Passwords donot match!'})

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']

class MyBoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'visibility', 'description', 'members']

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'visibility', 'description']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


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

class TaskSerializer(serializers.ModelSerializer):
    deadline = DateSerializer()
    reporter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task_id', 'title', 'description', 'status', 'priority', 'position', 'task_type', 'deadline', 'reporter']

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Column
        fields = ['id', 'title', 'position', 'tasks', 'deleted_at']


class ColumnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['title']

class TaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField(format=None, input_formats=None)
    reporter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'task_type', 'deadline', 'reporter']


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    members = UserSerializer(many=True)
    # columns = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'visibility', 'description', 'columns', 'members' ]

