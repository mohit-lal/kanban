from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


from .serializers import *
from .models import *
from .permissions import IsAuthenticatedAndHasAccessColumn

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


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(username=serializer.data.get('username'), password=serializer.data.get('password'))

        login(request, user)
        return Response({'status':'ok'}, 200)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'status':'ok'}, 200)

class BoardListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = MyBoardSerializer
    create_serializer_class = BoardCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def get_queryset(self):
        """
            shows board related to logged in users only.
        """
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

class ColumnListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = ColumnSerializer
    create_serializer_class = ColumnCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def get_queryset(self):
        return Column.objects.filter(board__id=self.kwargs.get('pk'), created_by=self.request.user, deleted_at__isnull=True)

    def perform_create(self, serializer):
        # create position by adding last_position + 1
        user = self.request.user

        last_created_column = Column.objects.filter(board__id=self.kwargs.get('pk'), deleted_at__isnull=True, created_by=user).first()
        
        new_position = 0

        if last_created_column:
            new_position = last_created_column.position + 1


        board = get_object_or_404(Board, pk=self.kwargs.get('pk'), created_by=user)
        serializer.save(board=board, created_by=user, position=new_position)

class ColumnRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return self.request.user.column_set.filter(board__id=self.kwargs.get('board_id'), created_by=self.request.user, deleted_at__isnull=True)
    
# class ColumnUpdatePositionAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [SessionAuthentication]

#     def get(self, request, *args, **kwargs):
#         new_position = self.request.GET.get('position')
#         # need validation?
#         # update prefix column, postfix column position.

#         prev_column = Column.objects.filter(position__gte=new_position).first()
#         if prev_column:
#             pass

    
class TaskCreateAPIView(CreateAPIView):
    """
        Only member users can add task to the column.
        and the creator themself.
    """
    model = Task
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticatedAndHasAccessColumn]
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        column = get_object_or_404(Column, pk=self.kwargs.get('pk'), deleted_at__isnull=True)

        serializer.save(column=column, reporter=user)

class BoardListAPIView(ListAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.request.user.boards.filter(deleted_at__isnull=True)

class BoardDetailAPIView(RetrieveAPIView):
    model = Board
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.request.user.boards\
            .filter(visibility=True, deleted_at__isnull=True)\
            .prefetch_related(Prefetch('columns', queryset=Column.objects.filter(deleted_at__isnull=True)))\
            .prefetch_related(Prefetch('columns__tasks', queryset=Task.objects.filter(deleted_at__isnull=True)))

class UserListView(ListAPIView):
    model = User
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        board = get_object_or_404(Board, pk=self.kwargs.get('pk'), created_by=self.request.user)
        users = User.objects.exclude(pk__in=[board.members.values_list('pk')]).exclude(pk=self.request.user.pk)
        return users
           