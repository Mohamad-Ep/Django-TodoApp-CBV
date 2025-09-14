from django.urls import path,include
from .views import TodoListApiView,TodoDetailsApiView
# ________________________________________________

app_name = 'api-v1'

urlpatterns = [
    path('todo/list/', TodoListApiView.as_view(), name='todo-list'),
    path('todo/<int:pk>/', TodoDetailsApiView.as_view(), name='todo-details'),
]

# ________________________________________________