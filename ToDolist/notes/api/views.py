from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import NoteSerializer
from ..models import Note, User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# class NoteAPIView(generics.ListAPIView):  # первый вариант API
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

# class NoteAPIView(APIView):
#     def get(self, request):
#         lst = Note.objects.all().values()
#         return Response({'posts': list(lst)})  # второй вариант, передается список всех объектов из БД (без сериализаторов)


# permissions`ы:
    # AllowAny - полный доступ
    # IsAuthenticated - только для auth.user
    # IsAdminUser - для тех, у кого админка
    # IsAuthenticatedOrReadOnly - для auth.user`s, а остальным только чтение

class NoteAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'  # в урле юзер сам может выбирать сколько записей на страницу
max_page_size = 10000  # ограничение page_size`а


class NoteAPIList(generics.ListAPIView):
    queryset = Note.objects.all() 
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # неавторизованным можно только читать
    pagination_class = NoteAPIListPagination

class NoteAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all() 
    serializer_class = NoteSerializer
    permission_classes = [ IsAuthenticated ]# IsOwnerOrReadOnly]  # менять может только owner
    # authentication_classes = [TokenAuthentication]  # можно указывать какие допускаются аутентификации

class NoteAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Note.objects.all() 
    serializer_class = NoteSerializer
    permission_classes = [IsAdminUser, IsAdminOrReadOnly]





# class NoteViewSet(viewsets.ModelViewSet):  # ReadOnlyModelViewSet - можно будет юзать только get запрос
    # queryset = Note.objects.all() 
    # serializer_class = NoteSerializer

#     def get_queryset(self):  # редакт. queryset`а, в данном случае вернули только 2 записи из бд
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Note.objects.all()[:2]  # при исп. данного метода можно убрать queryset, но тогда обязательно прописать basename в router.register
#         return Note.objects.filter(pk=pk)

#     @action(methods=['get'], detail=True) # allowed методы - get; detail False - список объектов а не один
#     def user_of_note(self, request, pk=None):  # теперь есть урл note/user_of_note (если detail True - note/1/user_of_note)
#         users = User.objects.get(pk=pk)
#         return Response({'users': users.username})       #[u.username for u in users]}) (при User.objects.all() и detail False)






# class NoteAPIList(generics.ListCreateAPIView):
    # queryset = Note.objects.all()
    # serializer_class = NoteSerializer


# class NoteAPIUpdate(generics.UpdateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

# class NoteAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer


# generics`ы:
    # CreateAPIView - создание данных по POST-запросу
    # ListAPIView - чтение списка данных по GET-запросу
    # RetrieveAPIView - чтение конкретных данных (записи) по GET-запросу
    # DestroyAPIView - удаление данных (записи) по DELETE-запросу
    # UpdateAPIView - изменение данных по PUT- или PATCH-запросу
    # ListCreateAPIView - для чтения (по GET-запросу) и создания списка данных (по POST-запросу)
    # RetrieveUpdateAPIView - чтение и изменение отдельной записи (GET- и POST-запрос)
    # RetrieveDestroyAPIView - чтение (GET-запрос) и удаление (DELETE-запрос) отдельной записи
    # RetrieveUpdateDestroyAPIView - чтение, изменение и добавление отдельной записи (GET, PUT, PATCH и DELETE запросы)


# class NoteAPIView(APIView):
#     def get(self, request):
#         n = Note.objects.all()
#         # many - для того чтобы была не одна запись. data для преобразования в json
#         return Response({'posts': NoteSerializer(n, many=True).data})

#     def post(self, request):
#         serializer = NoteSerializer(data=request.data)
#         # Проверка на валидность (при ошибке выдать ошибку)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()  # вызов метода create у сериализатора

#         # new_post = Note.objects.create(
#         #     title=request.data['title'],
#         #     description=request.data['description'],
#         #     datetodo=request.data['datetodo'],
#         #     user=request.data['user']
#         # )
#         # return`ит json строку
#         return Response({'post': serializer.data})

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': 'Метод put не разрешен'})

#         try:
#             instance = Note.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Объект не найден'})
#         # данные которые нужно изменить и у какого объекта (instance)
#         serializer = NoteSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()  # вызовет метод update т.к. передали 2 параметра
#         # отвечаем какие данные были изменены
#         return Response({'post': serializer.data})

#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': "Метод DELETE не разрешен"})

#         try:
#             instance = Note.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({'error': 'Объект не найден'})


#         return Response({'post': 'удалена запись' + str(pk)})
