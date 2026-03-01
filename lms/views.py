from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами.
    - Все действия требуют авторизации (IsAuthenticated).
    - Создание курса: разрешено только НЕ-модераторам (IsAuthenticated, ~IsModer).
    - Обновление курса: разрешено модераторам ИЛИ владельцу (IsAuthenticated, IsModer | IsOwner).
    - Удаление курса: разрешено только владельцу (IsAuthenticated, IsOwner).
    - Просмотр списка/деталей:
    - модераторы видят все курсы, остальные — только свои (через get_queryset()).
    """

    pagination_class = CoursePaginator

    def get_queryset(self):
        """
        Возвращает queryset курсов в зависимости от роли пользователя.
        - Модератор: все курсы.
        - Обычный пользователь: только курсы, где он владелец.
        """
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от action.
        - retrieve: детальный сериализатор курса.
        - остальные действия: базовый сериализатор курса.
        """

        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        При создании курса автоматически проставляет владельца текущим пользователем.
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Назначает permissions в зависимости от action.
        """
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание урока доступно только авторизованному пользователю,
    который не является модератором.
    При создании автоматически устанавливается владелец (owner).
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """
        Привязывает создаваемый урок к текущему пользователю.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Список уроков доступен только авторизованным пользователям.
    Видимость:
    - модератор видит все уроки,
    - обычный пользователь видит только свои уроки (owner=self.request.user).
    """

    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        """
        Возвращает queryset уроков в зависимости от роли пользователя.
        """
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр одного урока доступен авторизованному пользователю:
    модератору или владельцу урока.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление урока доступно авторизованному пользователю:
    модератору или владельцу урока.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока доступно только авторизованному владельцу урока.
    """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
