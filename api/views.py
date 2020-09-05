from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
        return user.board_set.filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BoardRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return self.request.user.board_set.filter(pk=self.kwargs.get('pk'), deleted_at__isnull=True)
    
class BoardAddMemberAPIView(RetrieveUpdateAPIView):
    """
        The user who created the board can only add 
        other members.
        Exception: cannot add self.

    """
    serializer_class = AddMemberSerializer
    model = Board
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['board'] = self.get_object()
        context['user'] = self.request.user
        return context

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'), created_by=self.request.user, deleted_at__isnull=True)

    def perform_update(self, serializer):
        serializer.save()




