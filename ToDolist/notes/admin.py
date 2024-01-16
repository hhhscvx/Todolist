from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created',
                    'datetodo', 'user']
    list_filter = ['status', 'created', 'user']
    search_fields = ['title', 'description', 'status', 'user__username']
