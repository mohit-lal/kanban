from django.urls import path
from .views import *

app_name = 'api'


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='test'),

    path('boards', BoardListCreateAPIView.as_view(), name='boards-list-create'),
]