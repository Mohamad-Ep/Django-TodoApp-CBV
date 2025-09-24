from celery import shared_task
from .models import Todo
from time import sleep

# ________________________________________________


@shared_task
def remove_complate_todo_after_10min():
    todos = Todo.objects.filter(is_done=True)
    todos.delete()
    print('Remove Complate Todos every 10 min ...')


# ________________________________________________
