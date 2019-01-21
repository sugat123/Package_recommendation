from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from .models import History
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from app.mixins import UserMixin

# Create your views here.
class HistoryView(UserMixin, ListView):
    print('in hisory')
    model = History
    template_name = 'history.html'

    def get_queryset(self):
        user_history = History.objects.filter(user = self.request.user)
        return user_history


class DeleteHistory(SingleObjectMixin, View):
    model = History

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        if obj is not None:
            obj.delete()
        return redirect('app:history')
