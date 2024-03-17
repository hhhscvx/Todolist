from django.urls import include, path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.list_view, name='list_view'),
    path('<int:note_id>/', views.detail_view, name='detail_view'),
    path('today/', views.list_today_view, name='list_today_view'),
    path('create/', views.note_create_view, name='create_view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('status/<int:pk>/<str:status>/',
         views.change_task_status, name="change-task-status")
]
