import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Todo
from accounts.models import CustomUser
# _______________________________________________

@pytest.mark.django_db
class TestTodoModel:
    def test_create_todo_model(self):
        user = CustomUser.objects.create_user(
            email = 'test12@gmail.com',
            password = 'Aa123456@',
            is_active = True,
            is_verficated = True)    
        todo = Todo.objects.create(title='todo model',author=user)
        assert Todo.objects.filter(pk=todo.pk).exists()
        assert todo.title == 'todo model'
# _______________________________________________