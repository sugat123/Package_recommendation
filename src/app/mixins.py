from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy


class UserMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app:index')
