from django import forms
from django.forms import TextInput, DateInput
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'datetodo', 'description']
        labels = {
            'title': 'Название',
            'datetodo': 'Дедлайн',
            'description': 'Описание',
        }
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Название...'}),
            'datetodo': DateInput(attrs={'placeholder': 'До какого числа выполнить...'}),
            'description': TextInput(attrs={'placeholder': 'Описание...'}),
        }
