from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def list_view(request):
    all_notes = Note.objects.all().order_by('-datetodo')
    return render(request, 'notes/list.html', {'all_notes': all_notes})


def detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/detail.html', {'note': note})


def list_today_view(request):
    today_notes = Note.objects.filter(datetodo=date.today())
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
