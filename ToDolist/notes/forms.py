from django import forms
from django.forms import TextInput, DateInput, Textarea
from .models import Note

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except ValidationError as error:
            self.add_error('password1', error)
        return password1


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
            'datetodo': DateInput(attrs={'placeholder': 'До какого числа выполнить...', 'type': 'date'}),
            'description': Textarea(attrs={'placeholder': 'Описание...'}),
        }
