import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from ..models import Todo
# ________________________________________________

### Fixture Functions

@pytest.fixture
def api_client():
    client = APIClient()
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
class TestTodoApiView:
    def test_get_todolist_response_ok(self,api_client,user_client):
        url = reverse('todos:api-v1:todo-list')
        api_client.force_authenticate(user=user_client)
        response = api_client.get(url)        
        assert response.status_code == 200
        
    def test_get_todo_details_response_ok(self,api_client,user_client):
        todo = Todo.objects.create(title='test todo')
        url = reverse('todos:api-v1:todo-details', kwargs={'pk':todo.pk})
        api_client.force_authenticate(user_client)
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_post_todo_response_201(self,api_client,user_client):
        url = reverse('todos:api-v1:todo-list')
        api_client.force_authenticate(user_client)
        data = {
            'title':'todo test1'
        }
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_put_todo_details_response_200(self,api_client,user_client):
        todo = Todo.objects.create(title='todo test')
        url = reverse('todos:api-v1:todo-details', kwargs={'pk':todo.pk})
        api_client.force_authenticate(user_client)
        data = {'title':'todo edit'}
        response = api_client.put(url,data)
        assert response.status_code == 200
# ________________________________________________