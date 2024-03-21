from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import json


def note_edit(request, note_id):
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        json_data = json.loads(request.body)
        new_title = json_data.get("new_title")
        new_datetodo_str = json_data.get("new_datetodo")
        new_description = json_data.get("new_description")
        if new_title:
            note.title = str(new_title)
            note.save()
        if new_datetodo_str:
            try:
                new_datetodo_str = new_datetodo_str.split(' ')
                day = new_datetodo_str[0]
                month = months[new_datetodo_str[1]]
                year = new_datetodo_str[2]
                new_datetodo = f'{year}-{month}-{day}'
                note.datetodo = new_datetodo
                note.save()
            except ValueError as err:
                print(f'Ошибка с датой: {err}')
                pass
        if new_description:
            note.description = new_description
            note.save()
        if new_title or new_datetodo or new_description:
            return redirect('notes:list_view')
    return JsonResponse({"success": True})


def note_delete(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    return redirect('notes:list_view')


def change_task_status(request, pk, status):
    note = Note.objects.get(pk=pk)
    note.status = str(status)
    note.save()
    return redirect('notes:list_view')


@login_required
def list_view(request):
    # по идеи должно быть datetodo без -, но я пока так оставлю, привычнее
    all_notes = Note.objects.filter(user=request.user).order_by('-datetodo')
    return render(request, 'notes/list.html', {'all_notes': all_notes})


@login_required
def detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def list_today_view(request):
    today_notes = Note.objects.filter(datetodo=date.today(), user=request.user)
    return render(request, 'notes/list_today.html', {'today_notes': today_notes})


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
            return redirect('notes:list_view')
    else:
        note = NoteForm()

    return render(request, 'notes/create.html', {'note': note})


def register_view(request):
    if request.method == 'POST':
        reg = UserCreationForm(request.POST)
        if reg.is_valid():
            reg.save()
            cd = reg.cleaned_data
            username = cd['username']
            password = cd['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('notes:list_view')
    else:
        reg = UserCreationForm()
    return render(request, 'registration/register.html', {'form': reg})
