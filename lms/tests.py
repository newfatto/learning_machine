from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson

User = get_user_model()


class LessonCRUDTestCase(APITestCase):
    """Минимальные тесты CRUD уроков и проверка прав доступа."""

    def setUp(self) -> None:
        self.owner = User.objects.create_user(email="owner@test.ru", password="12345")
        self.other = User.objects.create_user(email="other@test.ru", password="12345")

        self.moder = User.objects.create_user(email="moder@test.ru", password="12345")
        moderators_group, _ = Group.objects.get_or_create(name="moderators")
        self.moder.groups.add(moderators_group)

        self.course = Course.objects.create(name="Course 1", owner=self.owner)

        self.lesson = Lesson.objects.create(
            name="Lesson 1",
            description="Desc",
            course=self.course,
            owner=self.owner,
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        self.create_url = "/lesson/create/"
        self.list_url = "/lessons/"
        self.retrieve_url = f"/lesson/{self.lesson.id}/"
        self.update_url = f"/lesson/update/{self.lesson.id}/"
        self.delete_url = f"/lesson/delete/{self.lesson.id}/"

    def test_lesson_create_unauth_401(self) -> None:
        """Неавторизованный пользователь не может создавать урок."""
        data = {
            "name": "New lesson",
            "description": "Text",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=abc",
        }
        response = self.client.post(self.create_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_owner_201(self) -> None:
        """Обычный авторизованный пользователь (не модератор) может создать урок."""
        self.client.force_authenticate(user=self.owner)

        data = {
            "name": "New lesson",
            "description": "Text",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=abc",
        }
        response = self.client.post(self.create_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Lesson.objects.filter(name="New lesson", owner=self.owner).exists()
        )

    def test_lesson_create_moder_403(self) -> None:
        """Модератор не может создавать уроки."""
        self.client.force_authenticate(user=self.moder)

        data = {
            "name": "Moder lesson",
            "description": "Text",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=abc",
        }
        response = self.client.post(self.create_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_invalid_video_link_400(self) -> None:
        """Ссылка на видео должна быть только YouTube / youtu.be."""
        self.client.force_authenticate(user=self.owner)

        data = {
            "name": "Bad link lesson",
            "description": "Text",
            "course": self.course.id,
            "video_link": "https://example.com/video",
        }
        response = self.client.post(self.create_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_list_owner_200(self) -> None:
        """Обычный пользователь видит только свои уроки."""
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json().get("results", response.json())
        self.assertEqual(len(results), 1)

    def test_lesson_retrieve_owner_200(self) -> None:
        """Владелец может смотреть свой урок."""
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve_other_403(self) -> None:
        """Пользователь не может смотреть чужой урок."""
        self.client.force_authenticate(user=self.other)

        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner_200(self) -> None:
        """Владелец может обновлять урок."""
        self.client.force_authenticate(user=self.owner)

        data = {"name": "Lesson 1 updated"}
        response = self.client.patch(self.update_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Lesson 1 updated")

    def test_lesson_update_other_403(self) -> None:
        """Пользователь не может обновлять чужой урок."""
        self.client.force_authenticate(user=self.other)

        data = {"name": "Hacked"}
        response = self.client.patch(self.update_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_owner_204(self) -> None:
        """Только владелец может удалить урок."""
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
