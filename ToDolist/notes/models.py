from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    STATUS_CHOICES = [
        ('ToDo', 'Не сделано'),
        ('Completed', 'Сделано'),
    ]
    id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    datetodo = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='ToDo')
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='notes_created')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
