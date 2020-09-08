from django.urls import path
from .views import *

app_name = 'api'


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),

    
    path('my/boards', BoardListCreateAPIView.as_view(), name='my-boards-list-create'), #will only show boards created by logged in user. #done
    path('my/board/<int:pk>', BoardRetrieveUpdateDestroyAPIView.as_view(), name='my-board-retrieve-update-delete'),#done
    path('my/board/<int:pk>/add-members/', BoardAddMemberAPIView.as_view(), name='my-board-add-members'),

    path('my/board/<int:pk>/columns', ColumnListCreateAPIView.as_view(), name='my-list-create-columns'), #list-done, 
    path('my/board/<int:board_id>/column/<int:pk>', ColumnRetrieveUpdateDestroyAPIView.as_view(), name='my-column-retrieve-update-delete'),
    # path('column/<int:pk>/update-position', )

    path('column/<int:pk>/tasks', TaskCreateAPIView.as_view(), name='add-task-column'),  #done

    path('boards', BoardListAPIView.as_view(), name='boards-list'), #shows board the user is member of.
    path('board/<int:pk>', BoardDetailAPIView.as_view(), name='board-detail'),  #done
    path('board/<int:pk>/users', UserListView.as_view(), name='user-list'),

]