from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Todo
from .forms import TodoForm
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound

# ________________________________________________


class IndexView(TemplateView):
    template_name = 'todos/index.html'


# ________________________________________________


class TodoList(LoginRequiredMixin, ListView):
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user, is_active=True)


# ________________________________________________


class CreateTodoView(LoginRequiredMixin, FormView):
    template_name = 'todos/todo_create.html'
    form_class = TodoForm
    success_url = reverse_lazy('todos:todolist')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


# ________________________________________________

# class DeletodoView(LoginRequiredMixin,DeleteView):        # problem - Error
#     model = Todo
#     context_object_name = 'todo'
#     success_url = reverse_lazy('todos:todolist')

#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

#     def get_queryset(self):
#         return self.model.objects.filter(author=self.request.user)

# ------------------------------


class DeletodoView(LoginRequiredMixin, View):
    success_url = reverse_lazy('todos:todolist')

    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs['pk'])

        if todo.author == request.user:
            todo.delete()
            return redirect(self.success_url)
        return HttpResponseNotFound(content="صفحه موردنظر وجود ندارد")


# ________________________________________________


class UpdateTodoView(LoginRequiredMixin, UpdateView):
    template_name = 'todos/todo_update.html'
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todos:todolist')

    def get_queryset(self):
        """User permission for change object"""
        return Todo.objects.filter(author=self.request.user, is_active=True)


# ________________________________________________


class ComplateTodoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs['pk'])

        if todo.author != request.user:
            return HttpResponseNotFound(content="صفحه موردنظر وجود ندارد")

        if not todo.is_done:
            todo.is_done = True
            todo.save()
        else:
            todo.is_done = False
            todo.save()

        return redirect('todos:todolist')


# ________________________________________________
