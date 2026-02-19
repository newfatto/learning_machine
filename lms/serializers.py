from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):

    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "lesson_count",
        )


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
