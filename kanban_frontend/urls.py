from django.urls import path
from .views import *

app_name = 'frontend'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('login', LoginTemplateView.as_view(), name='login'),
    path('register', RegisterTemplateView.as_view(), name='register'),

    path('my/boards', MyBoardTemplateView.as_view(), name='my-boards'),
    path('my/board/create', MyBoardCreateTemplateView.as_view(), name='my-board-create'),
    path('my/board/<int:pk>', MyBoardDetailTemplateView.as_view(), name='my-board-detail'),
    path('my/board/<int:pk>/update', MyBoardUpdateTemplateView.as_view(), name='my-board-update'),
]