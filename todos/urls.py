from django.urls import path
from todos import views as views
# ________________________________________________

app_name = 'todos'

urlpatterns = [
    path('', views.IndexView.as_view(), name='todolist'),
    path('todolist/', views.TodoList.as_view(), name='todolist'),
]

# ________________________________________________