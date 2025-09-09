from django.urls import path
from todos import views as views
# ________________________________________________

app_name = 'todos'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('todolist/', views.TodoList.as_view(), name='todolist'),
    path('create-todo/', views.CreateTodoView.as_view(), name='create-todo'),
    path('delete-todo/<int:pk>/', views.DeletodoView.as_view(), name='delete-todo'),
    path('update-todo/<int:pk>/', views.UpdateTodoView.as_view(), name='update-todo'),
    path('complate-todo/<int:pk>/', views.ComplateTodoView.as_view(), name='complate-todo'),
]

# ________________________________________________