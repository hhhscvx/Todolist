"""ToDolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import notes.api.views as views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenObtainPairView, TokenVerifyView
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'note', views.NoteViewSet)  # basename='notee' - изменить маршруты
# print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls', namespace='notes')),

    # drf
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/note/', views.NoteAPIList.as_view()),
    path('api/v1/note/<int:pk>/', views.NoteAPIUpdate.as_view()),
    path('api/v1/notedelete/<int:pk>/', views.NoteAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  # djoser авторизация по post-запросам
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # авторизация по токенам
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # передав на этой странице данные пользователя, на jwt.io можно вписать токен и узнать его расшифровка
    path('api/v1/token/refresh/', TokenObtainPairView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/v1/', include(router.urls)),  #                                                                   get  / post  / get(одну запись)/ put / delete
    # path('api/v1/notelist', views.NoteViewSet.as_view({'get': 'list'})),  # метод отправки и метод из ViewSets: list/create/retrieve/update/destroy
    # path('api/v1/notelist/<int:pk>/', views.NoteViewSet.as_view({'put': 'update'})),  # вызовет put т.к. передали pk
]

# При DefaultRouter по адресу `api/v1/` - мы видим ссылку на api/v1/note (список api-маршрутов), а при SimpleRouter такого не происходит
