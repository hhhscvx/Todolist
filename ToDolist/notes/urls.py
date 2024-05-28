from django.urls import include, path
from . import views
from django.contrib.auth import urls

app_name = 'notes'

urlpatterns = [
    path('', views.list_view, name='list_view'),
    path('create/', views.note_create_view, name='create_view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('status/<int:pk>/<str:status>/',
         views.change_task_status, name="change-task-status"),
    path('delete/<int:pk>/', views.note_delete, name="note_delete"),
    path('edit/<int:note_id>/', views.note_edit, name="note_edit"),
]
