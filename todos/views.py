from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todo
# ________________________________________________

class IndexView(TemplateView):
    template_name = 'todos/index.html'
# ________________________________________________

class TodoList(LoginRequiredMixin,ListView):
    template_name = 'todos/todo_list.html'
    queryset = Todo.objects.filter(is_active=True)
    context_object_name = 'todos'
    
    # def get(self, request, *args, **kwargs):
    #     return render(self, self.template_name)
# ________________________________________________
