import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ..forms import TodoForm
# _______________________________________________

@pytest.mark.django_db
class TestTodoForm:
    def test_todo_form_data_valid(self):
        data = {'title':'todo form'}
        form = TodoForm(data)
        assert form.is_valid() == True
# ________________________________________________