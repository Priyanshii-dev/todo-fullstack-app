# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


class AuthAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_api_creates_user_and_returns_tokens(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "newuser@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["statusCode"], status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Registration successful")
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], "newuser@example.com")

    def test_register_api_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "Existing@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_login_api_returns_tokens_for_valid_credentials(self):
        User.objects.create_user(
            username="activeuser@example.com",
            email="activeuser@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "email": "activeuser@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["statusCode"], status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful")
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], "activeuser@example.com")

    def test_login_api_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "email": "missing@example.com",
                "password": "wrongpass",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
        self.assertEqual(
            response.data["message"],
            "Invalid email or password.",
        )


class TaskAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="taskuser@example.com",
            email="taskuser@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="otheruser@example.com",
            email="otheruser@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_update_task_api_edits_current_users_task(self):
        task = Task.objects.create(
            user=self.user,
            task="Old task",
            is_completed=False,
        )

        response = self.client.patch(
            f"/api/tasks/edit/{task.id}",
            {
                "task": "Updated task",
                "is_completed": True,
            },
            format="json",
        )

        task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.task, "Updated task")
        self.assertTrue(task.is_completed)
        self.assertEqual(response.data["task"], "Updated task")
        self.assertTrue(response.data["is_completed"])

    def test_list_task_api_returns_only_current_users_tasks(self):
        own_task = Task.objects.create(
            user=self.user,
            task="My task",
        )
        Task.objects.create(
            user=self.other_user,
            task="Other user's task",
        )

        response = self.client.get("/api/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], own_task.id)
        self.assertEqual(response.data[0]["task"], "My task")

    def test_table_task_api_returns_paginated_tasks(self):
        for index in range(7):
            Task.objects.create(
                user=self.user,
                task=f"My task {index + 1}",
            )

        response = self.client.post(
            "/api/tasks/",
            {
                "page": 2,
                "limit": 3,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["page"], 2)
        self.assertEqual(response.data["data"]["limit"], 3)
        self.assertEqual(response.data["data"]["total"], 7)
        self.assertEqual(response.data["data"]["totalPages"], 3)
        self.assertEqual(len(response.data["data"]["results"]), 3)

    def test_search_task_api_filters_by_name(self):
        Task.objects.create(user=self.user, task="Buy milk")
        Task.objects.create(user=self.user, task="Read book")

        response = self.client.post(
            "/api/tasks/search/",
            {"name": "milk"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["task"], "Buy milk")

    def test_filter_task_api_filters_by_completed_status(self):
        Task.objects.create(user=self.user, task="Done task", is_completed=True)
        Task.objects.create(user=self.user, task="Pending task", is_completed=False)

        response = self.client.post(
            "/api/tasks/filter/",
            {"is_completed": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertTrue(response.data["data"][0]["is_completed"])

    def test_create_task_api_assigns_current_user(self):
        response = self.client.post(
            "/api/tasks/create/",
            {
                "task": "Owned task",
                "is_completed": False,
            },
            format="json",
        )

        task = Task.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(task.user, self.user)
        
    def test_update_task_api_rejects_empty_task(self):
        task = Task.objects.create(
            user=self.user,
            task="Keep me valid",
        )

        response = self.client.patch(
            f"/api/tasks/edit/{task.id}",
            {"task": "   "},
            format="json",
        )

        task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(task.task, "Keep me valid")
        self.assertIn("task", response.data)

    def test_update_task_api_cannot_edit_another_users_task(self):
        task = Task.objects.create(
            user=self.other_user,
            task="Private task",
        )

        response = self.client.patch(
            f"/api/tasks/edit/{task.id}",
            {"task": "Changed by wrong user"},
            format="json",
        )

        task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(task.task, "Private task")

    def test_delete_task_api_deletes_current_users_task(self):
        task = Task.objects.create(
            user=self.user,
            task="Delete me",
        )

        response = self.client.delete(f"/api/tasks/delete/{task.id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_api_cannot_delete_another_users_task(self):
        task = Task.objects.create(
            user=self.other_user,
            task="Do not delete me",
        )

        response = self.client.delete(f"/api/tasks/delete/{task.id}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
