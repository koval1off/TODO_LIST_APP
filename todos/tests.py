from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from .models import Task
from .views import TaskListView
from .forms import UpdateTaskForm


class TodoTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

        cls.task = Task.objects.create(
            title = "Test Task",
            description = "Description",
            user = cls.user
        )

    def test_task_list_view_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)
        self.assertContains(response, "Tasks")
        self.assertTemplateUsed(response, "todos/task_list.html")

    def test_task_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/task/" % (reverse("account_login"))
        )
        response = self.client.get("%s?next=/task/" % (reverse("account_login")))
        self.assertContains(response, "LogIn")

    def test_task_list_view(self):
        view = resolve("/task/")
        self.assertEqual(view.func.__name__, TaskListView.as_view().__name__)
    
    def test_task_detail_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/task_detail.html")
        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)

    def test_task_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task_update", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/task_update.html")
        
    def test_task_update_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task_update", args=[self.task.id]))
        form = response.context.get("form")
        self.assertIsInstance(form, UpdateTaskForm)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_task_delete_view(self):
        pass

