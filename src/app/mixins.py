from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


class UserMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app:index')
