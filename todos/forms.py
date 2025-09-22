from django import forms
from .models import Todo

# ________________________________________________


class TodoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=250,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "placeholder": "تسک جدید را وارد کنید...",
            }
        ),
    )

    class Meta:
        model = Todo
        fields = ['title']


# ________________________________________________
