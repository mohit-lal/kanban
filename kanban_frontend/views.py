from django.views.generic import TemplateView

class IndexTemplateView(TemplateView):
    template_name = 'kanban_frontend/layouts/index.html'