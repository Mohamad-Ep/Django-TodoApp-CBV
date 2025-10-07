from django.urls import path, include
from .views import TodoListApiView, TodoDetailsApiView, get_weathermap

# ________________________________________________

app_name = 'api-v1'

urlpatterns = [
    path('todo/list/', TodoListApiView.as_view(), name='todo-list'),
    path('todo/<int:pk>/', TodoDetailsApiView.as_view(), name='todo-details'),
    # weather api
    path('weather/tehran/', get_weathermap, name='get-weather'),
]

# ________________________________________________
