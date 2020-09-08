from django.urls import path
from .views import *

app_name = 'frontend'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('login', LoginTemplateView.as_view(), name='login'),

    path('my/boards', MyBoardTemplateView.as_view(), name='my-boards'),
]