from rest_framework import generics
from .serializers import NoteSerializer
from ..models import Note

class NoteAPIView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
