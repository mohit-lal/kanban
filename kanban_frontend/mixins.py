from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class LoginRequired403Mixin(LoginRequiredMixin):
    login_url = reverse_lazy('frontend:login')