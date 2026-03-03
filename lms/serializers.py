from django.template.context_processors import request
from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import youtube_link_validator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[youtube_link_validator])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribe = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribe(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=obj).exists()

    class Meta:
        model = Course
        fields = ("name", "description", "lesson_count", "lessons", "is_subscribe")
