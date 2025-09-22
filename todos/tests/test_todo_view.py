import pytest
from django.urls import reverse
from ..models import Todo
from accounts.models import CustomUser
from django.test import Client
from ..forms import TodoForm
# _______________________________________________

### Fixture Functions

@pytest.fixture
def client():
    client = Client()
    return client

# -------------------------------

@pytest.fixture
def user_client():
    user = CustomUser.objects.create_user(
        email = 'test12@gmail.com',
        password = 'Aa123456@',
        is_active = True,
        is_verficated = True)    
    
    return user
# -------------------------------

@pytest.mark.django_db
class TestTodoView:
    def test_get_todolist_response_200(self,client,user_client):
        url = reverse('todos:todolist')
        client.force_login(user_client)
        response = client.get(url)
        assert response.status_code == 200
        
    def test_create_todo_response_302(self,client,user_client):
        url = reverse('todos:create-todo')
        client.force_login(user_client)
        data = {'title':'todo create'}
        response = client.post(url,data)
        assert response.status_code == 302
        
    def test_todo_delete_response_302(self,client,user_client):
        todo = Todo.objects.create(title='todo delete',author=user_client)
        url = reverse('todos:delete-todo', kwargs={'pk':todo.pk})
        client.force_login(user_client)
        response = client.get(url)
        assert response.status_code == 302
        
    def test_todo_update_response_200(self,client,user_client):
        todo = Todo.objects.create(title='todo assert',author=user_client)
        url = reverse('todos:update-todo', kwargs={'pk':todo.pk})
        client.force_login(user_client)
        data = {'title':'todo update'}
        response = client.put(url,data)
        assert response.status_code == 200
# _______________________________________________