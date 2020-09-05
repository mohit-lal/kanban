from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate
from rest_framework.response import Response

from .serializers import *

class TestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        print(request.user)
        pass

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.data)
        if user:
            login(request, user)
            return Response({'status':'ok'}, 200)

        return Response({'error':'Username or password incorrect!!'}, 400)

class BoardListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = BoardSerializer
    create_serializer_class = BoardCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return user.board_set.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)




