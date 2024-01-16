from django.shortcuts import render, get_object_or_404
from .models import Note


def list_view(request):
    all_notes = Note.objects.all()
    return render(request, 'notes/list.html', {'all_notes': all_notes})


def detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/detail.html', {'note': note})
