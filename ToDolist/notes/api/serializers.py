from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):  # ModelSerializer
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # по дефолту указан auth.user (чтоб сами не заполняли при post в api/v1/note)

    class Meta:
        model = Note
        fields = ['title', 'description', 'datetodo', 'user']  # все поля - '__all__'


# class NoteSerializer(serializers.Serializer):  # Serializer
#     title = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField(read_only=True)
#     datetodo = serializers.DateField(read_only=True)
#     status = serializers.CharField(
#         max_length=20, default='ToDo')
#     description = serializers.CharField()
#     user = serializers.IntegerField()

#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)

#     # instance - объект Note, а validated_data - словарь из данных которые нужно изменить в бд
#     def update(self, instance, validated_data):
#         # берем title из очищенных данных -> если его там нет берем из объекта модели (оставляем без изменений)
#         instance.title = validated_data.get("title", instance.title)
#         instance.datetodo = validated_data.get("datetodo", instance.datetodo)
#         instance.status = validated_data.get("status", instance.status)
#         instance.description = validated_data.get(
#             "description", instance.description)
#         instance.user = validated_data.get("user", instance.user)
#         instance.save()  # сохр. изменения
#         return instance
