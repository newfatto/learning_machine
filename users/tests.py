from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import Subscription

User = get_user_model()


class SubscriptionTestCase(APITestCase):
    """Тесты подписки:
    - пользователь авторизуется и создаёт курс
    - подписка на курс
    - получение списка курсов."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(email="user@test.ru", password="12345")

        self.courses_url = "/course/"
        self.subscriptions_url = "/users/subscriptions/"

    def create_course_as_user(self) -> Course:
        """
        Создаёт курс от лица self.user и возвращает объект Course из БД.
        Проверяет, что owner проставился автоматически.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.courses_url,
            data={"name": "Course 1", "description": "Desc"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course_id = response.json().get("id")
        self.assertIsNotNone(course_id)

        course = Course.objects.get(id=course_id)
        self.assertEqual(course.owner, self.user)
        return course

    def test_subscription_unauth_401(self) -> None:
        """Без авторизации подписки недоступны."""
        response = self.client.get(self.subscriptions_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription(self) -> None:
        """Пользователь создал курс -> подписался -> отписался."""
        course = self.create_course_as_user()

        # подписка добавлена
        response_add = self.client.post(
            self.subscriptions_url,
            data={"course": course.id},
            format="json",
        )
        self.assertEqual(response_add.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=course).exists()
        )

        # подписка удалена
        response_del = self.client.post(
            self.subscriptions_url,
            data={"course": course.id},
            format="json",
        )
        self.assertEqual(response_del.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=course).exists()
        )

    def test_subscription_list(self) -> None:
        """GET возвращает список подписок текущего пользователя."""
        course = self.create_course_as_user()

        Subscription.objects.create(user=self.user, course=course)

        response = self.client.get(self.subscriptions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["course"], course.id)
