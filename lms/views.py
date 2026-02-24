from rest_framework import generics, viewsets

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from lms.permissions import IsModer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    # def get_permissions(self)
    #     if self.action == 'list':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     elif self.action == 'create':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     elif self.action == 'retrieve':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     elif self.action == 'update':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     elif self.action == 'partial_update':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     elif self.action == 'destroy':
    #         self.permission_classes = [список пермишенов для этого эндпоинта]
    #     return [permission() for permission in self.permission_classes]




class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
