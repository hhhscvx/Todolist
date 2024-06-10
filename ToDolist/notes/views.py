from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import json
from django.conf import settings
from django.core.cache import cache
from .services.cache_delete import cache_delete


def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        # post data
        json_data = json.loads(request.body)
        new_title = json_data.get("new_title")
        new_datetodo_str = json_data.get("new_datetodo")
        new_description = json_data.get("new_description")
        # set data
        if new_title:
            note.title = str(new_title)
            note.save()
            cache_delete(cache, settings)
        if new_datetodo_str:
            try:
                # set correct date  # вот тут ваще тильт как все надо было в services перенести
                new_datetodo_str = new_datetodo_str.split(' ')
                day = new_datetodo_str[0]
                month = settings.MONTHS[(new_datetodo_str[1]).lower()]
                year = new_datetodo_str[2]
                new_datetodo = f'{year}-{month}-{day}'
                note.datetodo = new_datetodo
                note.save()
                cache_delete(cache, settings)
            except ValueError as err:
                print(f'Ошибка с датой: {err}')
                pass
        if new_description:
            note.description = new_description
            note.save()
            cache_delete(cache, settings)
        if new_title or new_datetodo or new_description:
            return redirect('notes:list_view')
    return JsonResponse({"success": True})


def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    cache_delete(cache, settings)
    return redirect('notes:list_view')


def change_task_status(request, pk, status):
    note = Note.objects.get(pk=pk)
    note.status = str(status)
    note.save()
    cache_delete(cache, settings)
    return redirect('notes:list_view')


@login_required
def list_view(request):
    if all_notes := cache.get(settings.NOTES_CACHE_NAME):  # GENIOUSSS SYNTAX???
        pass
    else:
        all_notes = Note.objects.filter(user=request.user).order_by('-datetodo')
        cache.set(settings.NOTES_CACHE_NAME, all_notes, 60 * 60)
    return render(request, 'notes/list.html', {'all_notes': all_notes})


@login_required
def note_create_view(request):
    if request.method == 'POST':
        note = NoteForm(request.POST)
        if note.is_valid():
            title = note.cleaned_data['title']
            description = note.cleaned_data['description']
            datetodo = note.cleaned_data['datetodo']
            new_note = Note.objects.create(
                title=title, description=description, datetodo=datetodo, user=request.user)
            messages.success(request, 'Заметка успешно добавлена')
            new_note.save()
            cache_delete(cache, settings)
            return redirect('notes:list_view')
    else:
        note = NoteForm()

    return render(request, 'notes/create.html', {'note': note})


def register_view(request):
    if request.method == 'POST':
        reg = CustomUserCreationForm(request.POST)
        if reg.is_valid():
            reg.save()
            cd = reg.cleaned_data
            username = cd['username']
            password = cd['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('notes:list_view')
    else:
        reg = CustomUserCreationForm()
    cache_delete(cache, settings)
    return render(request, 'registration/register.html', {'form': reg})
