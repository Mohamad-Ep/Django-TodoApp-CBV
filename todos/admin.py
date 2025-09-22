from django.contrib import admin
from .models import Todo

# ________________________________________________


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_date',
        'published_date',
        'is_active',
        'is_done',
        'author',
    )


# ________________________________________________
