from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = 'kanban_frontend/layouts/index.html'

class LoginTemplateView(TemplateView):
    template_name = 'kanban_frontend/auth/login.html'

class MyBoardTemplateView(TemplateView):
    template_name = 'kanban_frontend/board/my_boards.html'