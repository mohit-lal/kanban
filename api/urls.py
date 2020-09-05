from django.urls import path
from .views import *

app_name = 'api'


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='test'),

    path('boards', BoardListCreateAPIView.as_view(), name='boards-list-create'),
    path('board/<int:pk>', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-retrieve-update-delete'),
    path('board/<int:pk>/add-members/', BoardAddMemberAPIView.as_view(), name='board-add-members'),

    path('board/<int:pk>/columns', ColumnListCreateAPIView.as_view(), name='list-create-columns'),
    path('board/<int:board_id>/column/<int:pk>', ColumnRetrieveUpdateDestroyAPIView.as_view(), name='column-retrieve-update-delete')
]