from django.views.generic import TemplateView
from .mixins import LoginRequired403Mixin


class IndexTemplateView(TemplateView):
    template_name = 'kanban_frontend/layouts/index.html'

class LoginTemplateView(TemplateView):
    template_name = 'kanban_frontend/auth/login.html'

class RegisterTemplateView(TemplateView):
    template_name = 'kanban_frontend/auth/register.html'

class MyBoardTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/board/my_boards.html'

class MyBoardCreateTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/board/board_create.html'

class MyBoardDetailTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/board/board_detail.html'

class MyBoardUpdateTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/board/board_update.html'

class ProjectTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/projects/list.html'

class ProjectDetailTemplateView(LoginRequired403Mixin, TemplateView):
    template_name = 'kanban_frontend/projects/detail.html'